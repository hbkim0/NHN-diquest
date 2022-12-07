import argparse

import data_utils
import model

import mlflow
import mlflow.keras
from keras.callbacks import TensorBoard


def main(opt):

    artifacts_path = 'model'
    mlflow.set_tracking_uri('http://133.186.171.5:5002')

    #
    with mlflow.start_run() as run:

        num_users, num_items, users_input, items_input, y_train = data_utils.load_data(opt.data)
        ncf = model.get_model(num_users, num_items, y_train.shape[1], opt.n_embedding, opt.learning_rate)

        tb = TensorBoard(log_dir=opt.tensorboard_logdir)

        ncf.fit([users_input, items_input], y_train, validation_split=0.2, epochs=opt.epochs, batch_size=opt.batch_size, callbacks=[tb])

        # log hyper-params
        mlflow.log_param("epochs", opt.epochs)
        mlflow.log_param("batch_size", opt.batch_size)
        mlflow.log_param("lr", opt.learning_rate)

        # log architecture
        mlflow.log_param("embedding dimension", opt.n_embedding)

        # log metric
        mlflow.log_metric(f'val_rmse', ncf.history.history['val_root_mean_squared_error'][-1])
        mlflow.keras.log_model(ncf, artifact_path=artifacts_path)        

    model_uri_ = f"runs:/{run.info.run_id}/{artifacts_path}"
    mlflow.register_model(model_uri=model_uri_, name = "ncf", tags={'rmse': ncf.history.history['val_root_mean_squared_error'][-1], 'exp_id': opt.exp_id})


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='./data/input.csv')
    parser.add_argument('--epochs', type=int, default=2)
    parser.add_argument('--batch-size', type=int, default=258)
    parser.add_argument('--n-embedding', type=int, default=1)
    parser.add_argument('--learning-rate', type=float, default=0.001)
    parser.add_argument('--tensorboard-logdir', type=str, default='./results')
    parser.add_argument('--exp-id', type=str, default='')

    opt = parser.parse_args()
    return opt


if __name__ == "__main__":

    opt = parse_opt()
    main(opt)        