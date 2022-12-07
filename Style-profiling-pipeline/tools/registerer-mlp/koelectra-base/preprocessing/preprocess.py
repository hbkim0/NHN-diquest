import pandas as pd
import numpy as np
import sys
import math
import re
from kiwipiepy import Kiwi
from tqdm import tqdm
from collections import defaultdict

def read_category(filename):
    category = pd.read_csv(filename, delimiter=',', encoding='utf-8')
    category.drop(category.columns[category.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

    dic = {}
    # key: value = entry: category
    for column in category.columns:
        for entry in category[column]:
            if isinstance(entry, str):
                dic[entry] = column

    return dic

def read_description(filename):
    description = pd.read_csv(filename, delimiter='\t', encoding='utf-8')
    sentences = []
    for column in list(description.columns):
        sentences += list(description[column])
    return sentences

def clean_sentences(sentences):
    return [" ".join(re.sub('[^A-Za-z0-9가-힣]', ' ', sentence.replace('.', '. ')).split()) for sentence in sentences] # 중간에 제대로 안짤린거 최대한 극복

def match_category_to_sentences(sentences, category):# list of list of tuples(word, tag)
    entry_list = sorted(list(category.keys()), key=lambda x: len(x), reverse=True)
    new_sentences = []
    for sentence in sentences:
        tmp = []
        splited_sentence = sentence.split(' ')
        already_tagged = False # 2 단어짜리 entry 처리를 위한 flag
        for i, word in enumerate(splited_sentence):
            if already_tagged is True:
                already_tagged = False
                continue
            for entry in entry_list:
                if ' ' not in entry:
                    if entry in word:
                        tmp.append((word, category[entry]+'_B'))
                        break
                else: # 공백 포함된 entry의 _B 부분과 _I 부분을 처리하는 방법이 달라야한다.
                    if i < len(splited_sentence)-1:
                        if word == entry.split(' ')[0] and entry.split(' ')[1] in splited_sentence[i+1]:
                            tmp.append((word, category[entry]+'_B'))
                            tmp.append((splited_sentence[i+1], category[entry]+'_I'))
                            already_tagged = True
                            break
            else:
                tmp.append((word, 'O'))
        new_sentences.append(tmp)

    return new_sentences

#TODO 아직 Category랑 결합 제대로 안헀음
def match_category_to_sentences_with_kiwi(sentences, category, kiwidict_path):# list of list of tuples(word, tag)
    kiwi = Kiwi()
    kiwi.load_user_dictionary(kiwidict_path)
    kiwi.prepare()

    new_sentences = []

    for sentence in tqdm(sentences):
        kiwi_result = kiwi.analyze(sentence)
        # 스페이스바로 잘라진 어절의 시작 index 맵핑이 필요할 듯
        matches = [(m.group(0), (m.start(), m.end())) for m in re.finditer(r'\S+', sentence)]

        idx_to_eojeol = {}
        match_idx = 0
        for i in range(len(sentence)):
            if i >= matches[match_idx][1][1]: # matches안의 어절의 마지막 position보다 i가 작을 때는
                match_idx += 1
            idx_to_eojeol[i] = match_idx


        for_ner = [[eojeol, "O"] for eojeol, indices in matches] # new_sentences list에 append할 때 사용하는 임시 list

        for morph_candidate, tag, start_idx, length in kiwi_result[0][0]:
            morph = morph_candidate.strip()
            if morph in category:
                if len(morph) == 1:
                    if tag != 'NNP' or tag != 'NNG': # 면, 마, 울 등 처리하기 위함
                        continue

                for_ner[idx_to_eojeol[start_idx]][1] = category[morph]+'_B'
                if len(morph.split(' ')) > 1: # 슬림 스트레이트 등 2개 이상으로 쪼개지는 경우
                    indices = [i+1 for i, x in enumerate(morph) if x == ' '] #2개 이상 쪼개졌을 때 스페이스바 바로 다음 단어들의 index
                    for index in indices:
                        for_ner[idx_to_eojeol[start_idx+index]][1] = category[morph]+'_I'
        new_sentences.append(for_ner)

    return new_sentences


def data_into_file(data, filename):
    with open(filename, 'w') as f:
        for line in data:
            for (word, tag) in line:
                if word == '울' or word == '면': # 울이랑 면 하드코딩
                    f.write(word+' '+'Material_B'+'\n')
                else:
                    f.write(word+' '+tag+'\n')
            f.write('\n')

def make_kiwi_dict(category_dict, result_path):
    with open(result_path, 'w') as f:
        for k, v in category_dict.items(): # entry, category 꼴
            if v != 'Fit' and v != 'Mood': #우선 fit이랑 무드는 제외
                f.write(k+'\t'+'NNG'+'\t'+'0'+'\n') # 우선 가장 높은 점수로, 전부다 일반명사로 박아보자
            else:
                f.write(k+'\t'+'MAG'+'\t'+'0'+'\n') # 우선은 부사로 박아두는데 나중에 후처리가 필요할 듯?

def convert_into_excel(excel_dir, category, kiwidict_path):
    kiwi = Kiwi()
    kiwi.load_user_dictionary(kiwidict_path)
    kiwi.prepare()

    final_frame = pd.DataFrame(columns=['title', 'image', 'url', 'originaldesc', 'siteinfo'])
    kiwi_frame = pd.DataFrame(columns=['Description', 'Category', 'Gender', 'Pattern', 'Season', 'Fit', 'Color', 'Material', 'Neckline', 'Mood'])

    cur_dir = os.path.join(os.getcwd(), "visualization")
    for excel_file in os.listdir(cur_dir):
        if excel_file.endswith('.xlsx'):
            data = pd.read_excel(os.path.join(cur_dir, excel_file))
            data = data.rename(columns={"img": "image", "desc": "originaldesc"})
            if '헤누지' in excel_file or 'Minibbong' in excel_file or 'Style' in excel_file:
                data['siteinfo'] = '여자'
            else:
                data['siteinfo'] = '남자'
            final_frame = final_frame.append(data, ignore_index=True)

    final_frame = final_frame.loc[:, ~final_frame.columns.str.contains('^Unnamed')]

    sentences = [" ".join(re.sub('[^A-Za-z0-9가-힣]', ' ', sentence.replace('.', '. ')).split()) for sentence in final_frame.originaldesc] # 전처리

    for sentence in tqdm(sentences):
        dic_for_pandas = defaultdict(list)
        kiwi_result = kiwi.analyze(sentence)
        # 스페이스바로 잘라진 어절의 시작 index 맵핑이 필요할 듯
        matches = [(m.group(0), (m.start(), m.end())) for m in re.finditer(r'\S+', sentence)]
        for morph_candidate, tag, start_idx, length in kiwi_result[0][0]:
            morph = morph_candidate.strip()
            if morph in category:
                if len(morph) == 1:
                    if tag != 'NNP' or tag != 'NNG': # 면, 마, 울 등 처리하기 위함
                        continue

                if category[morph] in kiwi_frame.columns: # 옷 종류가 아닐 경우
                    dic_for_pandas[category[morph]].append(morph)
                else:
                    dic_for_pandas['Category'].append(morph)

        for k, v in dic_for_pandas.items():
            dic_for_pandas[k] = ','.join(list(set(v))) # 중복 제거
        dic_for_pandas['Description'] = sentence
        kiwi_frame = kiwi_frame.append(dic_for_pandas, ignore_index=True)

    return pd.concat([final_frame, kiwi_frame], axis=1)


if __name__ == '__main__':
    import openpyxl as ox
    import os
    crwaling_descriptions = []
    excel_visualizations = []
    cur_dir = os.path.join(os.getcwd(), "labeling/crawling_data")
    for excel_file in os.listdir(cur_dir):
        if excel_file.endswith('.xlsx'):
            file_name = os.path.join(cur_dir, excel_file)
            for i, row in enumerate(ox.load_workbook(file_name, read_only=True).worksheets[0].rows):
                if i == 0:
                    continue
                # print(row[-1].value)
                crwaling_descriptions.append(row[-1].value.replace('x000D', ' ')) # excel에서의 carriage return 처리

    category_filename = 'labeling/fashion_category_1012_english.csv'
    description_filename = 'labeling/description.tsv'
    kiwidict_path = 'kiwidict/userDict.txt'

    category = read_category(category_filename) # dictionary 형태로 반환
    sentences = clean_sentences(read_description(description_filename))
    final_sentences = sentences + clean_sentences(crwaling_descriptions)

    # # For excel visualization
    # excel_to_write = convert_into_excel('visualization', category, kiwidict_path)
    # excel_to_write.to_excel('labeling/result/1021_visualization.xlsx', encoding='utf-8-sig')







    make_kiwi_dict(category, kiwidict_path) # kiwidict 만들고
    output = match_category_to_sentences_with_kiwi(final_sentences, category, kiwidict_path)

    from random import shuffle
    shuffle(output)

    train, dev = output[:int(len(output) * 0.9)], output[int(len(output) * 0.9):]

    data_into_file(data=train, filename='labeling/1022result/train.txt')
    data_into_file(data=dev, filename='labeling/1022result/dev.txt')


    # data_into_file(data=output, filename='result/mini_test.txt')
