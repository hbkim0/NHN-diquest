import pathlib 
import database
import pandas as pd

import config
import pydash as py_

from sklearn.preprocessing import LabelEncoder


# get_loaders
history_examples = database.get_history()


def get_attribute(attributes, key):
    return [ str(sorted(dict_['values'])) for dict_ in attributes if dict_['key'] == key].pop()
#
test = 0
# history
rows = []
for history in history_examples:
    customer_id = py_.get(history, 'customer')
    product_id = py_.get(history, 'product')
    rating = py_.get(history, 'rating')

    product = database.get_product(product_id)
    customer = database.get_customer(customer_id)

    if product is not None and customer is not None:

        # history columns
        history_row = {
            'customer_id': customer_id,
            'product_id': product_id,
            'rating': rating
        }

        # product columns
        attributes = py_.get(product, 'attributes')
        product_row = {
            'product_label': py_.get(product, 'label'),       
            'product_category': get_attribute(attributes, '카테고리'),
            'product_length': get_attribute(attributes, '기장'),
            'product_style': get_attribute(attributes, '스타일'), 
            'product_gender': py_.get(product,'gender'),
            'product_pattern': get_attribute(attributes, '패턴'),
            'product_season': get_attribute(attributes, '시즌'),
            'product_fit': get_attribute(attributes, '핏'),
            'product_color': get_attribute(attributes, '색상'),
            'product_material': get_attribute(attributes, '소재'),
            'product_neckline': get_attribute(attributes, '넥라인'),
        }

        customer_row = {
            'customer_gender': py_.get(customer, 'gender'),
            'customer_zipcode': py_.get(customer, 'zip_code'),
        }

        history_row.update(product_row)
        history_row.update(customer_row)

        rows.append(history_row)

        test+=1
        if test > 5000:
            break
    else:
        pass

# dataframe
df = pd.DataFrame(rows)

for col in list(df.columns):
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

df.to_csv('./input.csv', index=False)


