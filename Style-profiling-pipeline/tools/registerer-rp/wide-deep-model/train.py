import pandas as pd
import argparse

from keras.callbacks import TensorBoard
import mlflow
import mlflow.keras

from model import wide_deep



def main(opt):

    artifacts_path = 'model'
    mlflow.set_tracking_uri('http://133.186.171.5:5002')

    # 
    with mlflow.start_run() as run:
        data = pd.read_csv(opt.data)

        info = {
            'wide_categ' : ['customer_id','product_id'],
            'wide_conti' : [],
            'deep_categ' : ['customer_id','product_id', 'product_label', 'product_category', 'product_length', 
                            'product_style', 'product_gender', 'product_pattern', 'product_season', 
                            'product_fit', 'product_color', 'product_material', 'product_neckline', 
                            'customer_gender','customer_zipcode'],
            'deep_conti' : [],
            'target' : 'rating'
        }

        
        data['IS_TRAIN'] = 1

        layer_sizes = [opt.layer_size_1, opt.layer_size_2, opt.layer_size_3]

        wide_deep_model, X_train_wide_deep, y_train = wide_deep(data, info, layer_sizes, opt.n_embedding, opt.learning_rate)
            
        tb = TensorBoard(log_dir=opt.tensorboard_logdir)

        wide_deep_model.fit(X_train_wide_deep, y_train, validation_split=0.2, epochs=opt.epochs, batch_size=opt.batch_size, callbacks=[tb])

        # log hyper-params
        mlflow.log_param("epochs", opt.epochs)
        mlflow.log_param("batch_size", opt.batch_size)
        mlflow.log_param("lr", opt.learning_rate)

        # log architecture
        mlflow.log_param("embedding dimension", opt.n_embedding)

        # log metric
        mlflow.log_metric(f'val_rmse', wide_deep_model.history.history['val_root_mean_squared_error'][-1])
        mlflow.keras.log_model(wide_deep_model, artifact_path=artifacts_path)

    model_uri_ = f"runs:/{run.info.run_id}/{artifacts_path}"
    mlflow.register_model(model_uri=model_uri_, name = "wide-deep", tags={'rmse': wide_deep_model.history.history['val_root_mean_squared_error'][-1], 'exp_id': opt.exp_id})

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='./data/input.csv')
    parser.add_argument('--epochs', type=int, default=2)
    parser.add_argument('--batch-size', type=int, default=258)
    parser.add_argument('--learning-rate', type=float, default=0.001)
    parser.add_argument('--layer-size-1', type=int, default=16)
    parser.add_argument('--layer-size-2', type=int, default=8)
    parser.add_argument('--layer-size-3', type=int, default=4)
    parser.add_argument('--n-embedding', type=int, default=1)
    parser.add_argument('--tensorboard-logdir', type=str, default='./results')
    parser.add_argument('--exp-id', type=str, default='')

    opt = parser.parse_args()
    return opt

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)        