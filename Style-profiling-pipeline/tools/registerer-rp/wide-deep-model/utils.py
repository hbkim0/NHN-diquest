import pandas as pd
import numpy as np
import tensorflow.keras as keras


def wide_component(train, info):
    df_wide = train

    wide_cols = info['wide_categ'] + info['wide_conti']
    target = info['target']
    #concat target    
    df_wide = df_wide[wide_cols + [target] + ['IS_TRAIN']]

    #onehot encoding categ
    dummy_cols = [wc for wc in wide_cols if wc in info['wide_categ']]
    df_wide = pd.get_dummies(df_wide, columns=dummy_cols)

    train = df_wide[df_wide.IS_TRAIN == 1].drop('IS_TRAIN', axis=1)

    cols = [c for c in train.columns if c != target]
    X_train = train[cols].values
    X_train_wide = np.array(X_train, dtype=np.float)

    return X_train_wide


def deep_component(train, info, n_embedding):
    df_deep = train

    deep_cols = info['deep_categ'] + info['deep_conti']
    target = info['target']
    
    #embedding
    embedding_cols = info['deep_categ']

    df_deep = df_deep[deep_cols + [target, 'IS_TRAIN']]
    col_to_unique_val_num = dict(df_deep.nunique())
    train = df_deep[df_deep.IS_TRAIN == 1].drop('IS_TRAIN', axis=1)

    embeddings_tensors = []
    for ec in embedding_cols:
        layer_name = ec + '_inp'
        inp = keras.Input(shape=(1,), dtype='int64', name=layer_name)
        embd = keras.layers.Embedding(col_to_unique_val_num[ec], n_embedding, input_length=1)(inp)
        embeddings_tensors.append((inp, embd))
        del (inp, embd)

    continuous_tensors =[]
    for cc in info['deep_conti']:
        layer_name = cc + '_in'
        inp = keras.Input(shape=(1,), dtype='float32', name=layer_name)
        bulid = keras.layers.Reshape((1, 1))(inp)
        continuous_tensors.append((inp, bulid))
        del (inp, bulid)    

    X_train_deep = [train[c] for c in deep_cols]
    y_train_deep = np.array(train[target].values).reshape(-1, 1) 

    return X_train_deep, y_train_deep, embeddings_tensors, continuous_tensors