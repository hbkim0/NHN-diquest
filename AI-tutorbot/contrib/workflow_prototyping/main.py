import argparse
import random

import imutils
import cv2

import torch

from imutils.perspective import four_point_transform

from database import get_db


def parse_opt():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--', type=, default='')
    parser.add_argument('--photo-path', type=str, default='sample.jpg')

    opt = parser.parse_args()
    return opt


def main(opt):
    page = detect_page(opt.photo_path)
    page_dict = search_page(page)
    

    scoring_results = scoring(page, page_dict)

    results = {
        'workbook': page_dict['book_name'], 
        'page': page_dict['page_num'], 
        'results': scoring_results
    }
    print(results)


def detect_page(photo_path):
    photo = cv2.imread(photo_path)
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, [int(photo.shape[1]/2), int(photo.shape[0]/2)])
    _, gray = cv2.threshold(gray, 110, 255, cv2.THRESH_TOZERO)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    gray = cv2.edgePreservingFilter(gray, flags=1, sigma_s=45, sigma_r=0.2)
    edged = cv2.Canny(gray, 75, 200, True)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    findCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            findCnt = approx
            break

    if findCnt is None:
        raise Exception(('could not find outline'))

    contour_image = photo.copy()
    findCnt *= 2
    cv2.drawContours(contour_image, [findCnt], -1, (0, 255, 0), 2)

    output = photo.copy()
    transform_image = four_point_transform(output, findCnt.reshape(4, 2))
    cv2.imwrite('temp/detect.png', transform_image)
    return transform_image


def search_page(page):
    db = get_db()
    page_col = db['page']
    
    # input = preprocess(page)
    # vector = siamese_model(input)  # 모델 사용해서 벡터 획득
    vector = torch.tensor([0.5, 0.5, 0.5]).unsqueeze(0)  # 지금은 고정값으로
    best_sim = 0
    for page_dict in page_col.find():
        target = torch.tensor(page_dict['page_vector']).unsqueeze(0)
        sim = torch.cosine_similarity(target, vector)
        if sim > best_sim:
            best_sim = sim
            best_dict = page_dict

    print(f'similarity: {best_sim}')
    return best_dict


def scoring(page, page_dict):
    page = cv2.resize(page, (page_dict['page_width'], page_dict['page_height']))

    cv2.imwrite('temp/resize.jpg', page)
    boxed = page.copy()

    scoring_results = []
    for prob in page_dict['probs']:
        answers = []
        for answer in prob['answers']:
            bbox = answer['bbox']
            cv2.rectangle(boxed, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 5)  # for debug
            area = page[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            cv2.imwrite(f'temp/prob_{prob["prob_num"]}.jpg', area)

            # recog_result = ocr_model(area)  # 인식 모델 전체
            # pred = postprocess(recog_result)  # score가 가장 높은 것을 선택해서 type변환까지 수행
            pred = random.randrange(1, 10)
            answers.append({
                'answer_id': answer['answer_id'], 
                'label': answer['label'], 
                'prediction': pred, 
            })

        correct = True
        for i in answers:
            if i['label'] != i['prediction']:
                correct = False
                break

        scoring_result = {
            'prob_num': prob['prob_num'], 
            'correct': correct, 
            'answers': answers
        }
        scoring_results.append(scoring_result)

    cv2.imwrite('temp/result.jpg', boxed)
    return scoring_results


if __name__ == '__main__':
    opt = parse_opt()
    main(opt)
