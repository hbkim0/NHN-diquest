from utils import wide_component, deep_component

import tensorflow.keras as keras


# dict로 변환
def wide_deep(train, info, layer_sizes, n_embedding, lr):
    X_train_wide = wide_component(train, info)
    X_train_deep, y_train_deep, embeddings_tensors, continuous_tensors = deep_component(train, info, n_embedding)

    #make input 
    X_train_wide_deep = [X_train_wide] + X_train_deep
    y_train_wide_deep = y_train_deep

    deep_input = [et[0] for et in embeddings_tensors] + [ct[0] for ct in continuous_tensors]
    deep_embedding = [et[1] for et in embeddings_tensors] + [ct[1] for ct in continuous_tensors]
    deep_embedding = keras.layers.Flatten()(keras.layers.concatenate(deep_embedding))
    wide_input = keras.Input(shape=(X_train_wide.shape[1],), dtype='float32', name='wide')

    #dnn layer
    dnn_layer_1 = keras.layers.Dense(units=layer_sizes[0], activation='LeakyReLU')(deep_embedding)
    dnn_layer_2 = keras.layers.Dense(units=layer_sizes[1], activation='LeakyReLU')(dnn_layer_1)
    dnn_layer_3 = keras.layers.Dense(units=layer_sizes[2], activation='LeakyReLU')(dnn_layer_2)

    #
    wd_input = keras.layers.concatenate([wide_input, dnn_layer_3])
    wd_output = keras.layers.Dense(y_train_wide_deep.shape[1], activation='softmax', name='wide_deep')(wd_input)

    #
    wide_deep_model = keras.Model([wide_input, deep_input], wd_output)
    wide_deep_model.compile(optimizer=keras.optimizers.RMSprop(learning_rate=lr), loss='mse', metrics=[keras.metrics.RootMeanSquaredError()])    

    return wide_deep_model, X_train_wide_deep, y_train_wide_deep