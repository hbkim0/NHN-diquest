import pandas as pd
import numpy as np


def load_data(src_path):
    df = pd.read_csv(src_path, usecols=['customer_id', 'product_id', 'rating'])

    #
    num_users =  len(set(df['customer_id'])) + 1
    num_items =  len(set(df['product_id'])) + 1

    #
    users_input = df['customer_id'].values
    items_input = df['product_id'].values

    #
    y_train = np.array(df['rating'].values).reshape(-1, 1)

    return num_users, num_items, users_input, items_input, y_train
