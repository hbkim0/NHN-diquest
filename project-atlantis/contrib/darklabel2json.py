import argparse
from pathlib import Path
import shutil
import json


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--anno-path', type=str, required=True)
    parser.add_argument('--output-path', type=str, default='output')
    parser.add_argument('--remove-exist', action='store_true')
    parser.add_argument('--workbook-type', type=str, default='티플레이스')  # [티플레이스, 팩토연산]

    opt = parser.parse_args()
    return opt


def main(opt):
    print(opt)
    anno_path_list = Path(opt.anno_path).glob('**/*.txt')

    if opt.remove_exist:
        shutil.rmtree(opt.output_path)
    Path(opt.output_path).mkdir(parents=True, exist_ok=True)
    
    cnt = 0
    for anno_path in anno_path_list:
        cnt += 1

        print(anno_path)
        workbook_num, page_num = anno_path.stem.split('_')  # 티플레이스에서 workbook_num은 항상 동일
        
        with open(anno_path, 'r') as f:
            anno_list = f.readlines()
        
        probs = {}
        for anno in anno_list:
            anno = anno.split(',')
            prob_num, label = anno[0].split(':')
            bbox = [int(x) for x in anno[1:5]]

            answer = {'bbox': bbox, 'label': label}

            if probs.get(prob_num) == None:
                probs[prob_num] = {
                    'prob_num': prob_num, 
                    'answers': [answer]
                }
            else:
                probs[prob_num]['answers'].append(answer)
        
        new_anno = {
            'page_num': page_num, 
            'probs': list(probs.values())
        }
        with open(Path(opt.output_path, anno_path.stem).with_suffix('.json'), 'w', encoding='utf-8') as f:
            json.dump(new_anno, f, ensure_ascii=False, indent=4)

    if cnt == 0:
        print('txt file not found')
    else:
        print(f'{cnt} converted')
        if opt.workbook_type == '티플레이스':
            workbook_name = opt.workbook_type + '_' + workbook_num
            workbook_anno = {
                'name': workbook_name, 
                'no_pages': cnt
            }
            with open(Path(opt.output_path, workbook_name).with_suffix('.json'), 'w', encoding='utf-8') as f:
                json.dump(workbook_anno, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)