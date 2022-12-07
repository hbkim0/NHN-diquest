import pandas as pd
import glob
import os

def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

# 상품 품번의 숫자가 중복값도 있으며, 없는 번호도 존재한다. 따라서 이를 수정하고자 한다.
# 수정방법: 품번, 상품이미지를 새롭게 세팅.

df_product = pd.read_csv('./product_date.csv')
df_history = pd.read_csv('./history.csv')

unique_identifier = list(set(df_product['품번']))
unique_total_n = len(set(df_product['품번']))
unique_switch = list(range(1, unique_total_n+1))

modified = []

# get unique row
rows = []
for identifier in unique_identifier:
    # 품번 identifier 1 , 상품 이미지 index 3
    row = df_product[df_product['품번'] == identifier].values.tolist().pop()
    original_image_name = df_product[df_product['품번'] == identifier].values.tolist().pop()[3]
    # new identifier 
    new_identifier = unique_switch[0]
    new_image_name = str(new_identifier) + '.png'
    # 실제 상품 이미지 이름 변경, 복사
    image_path = glob.glob(f'./images/*/{original_image_name}').pop()
    os.system(f'cp {image_path} ./images/files/{new_image_name}')
    # product update
    row[1] = new_identifier
    row[3] = new_image_name
    rows.append(row)
    # history update
    df_history.loc[df_history['품번'] == identifier, '품번'] = new_identifier
    del unique_switch[0]



df = pd.DataFrame(rows)
df.columns = list(df_product.columns)

# 상품 품번 없는 것은 history에서 삭제.
identifier_product = list(set(df['품번']))
identifier_history = list(set(df_history['품번']))

diff_identifier = Diff(identifier_history, identifier_product)
for i in diff_identifier:
    df_history = df_history[df_history.품번 != i]


df.to_csv('./fix_product_date.csv', index=False)
df_history.to_csv('./fix_history.csv', index=False)