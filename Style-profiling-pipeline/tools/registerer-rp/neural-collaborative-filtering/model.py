from keras.layers import Embedding, Input, Dense, Concatenate, Flatten, Multiply
from keras.regularizers import l2
from keras.models import Model
import tensorflow.keras as keras



def get_model(num_users, num_items, y_train_dim, mf_dim, lr):

    #
    reg_mf = 0
    reg_layers=[0]
    layers=[10]    
    num_layer = len(layers)

    #
    user_input = Input(shape=(1,), dtype='int32', name = 'user_input')
    item_input = Input(shape=(1,), dtype='int32', name = 'item_input')    

    # Embedding layer
    MF_Embedding_User = Embedding(input_dim = num_users, output_dim = mf_dim, name = 'mf_embedding_user',
                                    embeddings_initializer='uniform', embeddings_regularizer = l2(reg_mf), input_length=1)

    MF_Embedding_Item = Embedding(input_dim = num_items, output_dim = mf_dim, name = 'mf_embedding_item',
                                    embeddings_initializer='uniform', embeddings_regularizer = l2(reg_mf), input_length=1)   

    MLP_Embedding_User = Embedding(input_dim = num_users, output_dim = int(layers[0]/2), name = "mlp_embedding_user",
                                    embeddings_initializer='uniform', embeddings_regularizer = l2(reg_layers[0]), input_length=1)
    MLP_Embedding_Item = Embedding(input_dim = num_items, output_dim = int(layers[0]/2), name = 'mlp_embedding_item',
                                    embeddings_initializer='uniform', embeddings_regularizer = l2(reg_layers[0]), input_length=1)   

    # MF part
    mf_user_latent = Flatten()(MF_Embedding_User(user_input))
    mf_item_latent = Flatten()(MF_Embedding_Item(item_input))
    mf_vector = Multiply()([mf_user_latent, mf_item_latent])

    # MLP part 
    mlp_user_latent = Flatten()(MLP_Embedding_User(user_input))
    mlp_item_latent = Flatten()(MLP_Embedding_Item(item_input))
    mlp_vector = Concatenate()([mlp_user_latent, mlp_item_latent])

    for idx in range(1, num_layer):
        layer = Dense(layers[idx], kernel_regularizer = l2(reg_layers[idx]), activation='relu', name="layer%d" %idx)
        mlp_vector = layer(mlp_vector)

    predict_vector = Concatenate()([mf_vector, mlp_vector])    

    prediction = Dense(y_train_dim, activation='softmax', name = "prediction")(predict_vector)

    model = Model(inputs=[user_input, item_input], outputs=prediction)
    model.compile(optimizer=keras.optimizers.RMSprop(learning_rate=lr), loss='mse', metrics=[keras.metrics.RootMeanSquaredError()])    

    return model


