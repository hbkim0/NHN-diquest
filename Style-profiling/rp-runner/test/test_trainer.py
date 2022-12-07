import pathlib
import config
import docker

#docker run --rm -it --ipc=host -v /data/juhwan/project-mamihlapinatapai/rp-runner/test/data:/usr/src/datasets -v /ml_data/mamihlapinatapai/tracking-server:/usr/src/app/tracking-server -v /data/juhwan/project-mamihlapinatapai/rp-runner/results:/usr/src/app/exp_results wide_deep:latest
#python train.py --data ../datasets/input.csv --tensorboard-logdir exp_results --epochs 2 --batch-size 128 --layer-size-1 6 --layer-size-2 3 --layer-size-3 1 --n-embedding 1 --learning-rate 0.001
def wide_deep_run():

    image_name = 'wide_deep:latest'
    epoch=20
    batch_size=128
    layer_sizes_1 = 6
    layer_sizes_2 = 4
    layer_sizes_3 = 2
    n_embedding = 1
    learning_rate = 0.001

    loader_dir = '/data/juhwan/project-mamihlapinatapai/rp-runner/test/data'
    result_base_dir = '/data/juhwan/project-mamihlapinatapai/rp-runner/test/results'

    tracking_server_dir = pathlib.Path(config.TRACKING_SERVER_BASE_PATH)

    client = docker.from_env()

    volumes = [
        f'{str(tracking_server_dir)}:/usr/src/app/tracking-server', 
        f'{str(loader_dir)}:/usr/src/datasets',
        f'{str(result_base_dir)}:/usr/src/app/exp_results',
    ]    

    #
    if config.SUPPORT_GPU:
        device_requests = [docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])]
    else:
        device_requests = None

    #
    cli_command = [
        ' '.join([
            'python train.py',
            '--data ../datasets/input.csv',
            '--tensorboard-logdir exp_results',
            f'--epochs {epoch}',
            f'--batch-size {batch_size}',
            f'--layer-size-1 {layer_sizes_1}',
            f'--layer-size-2 {layer_sizes_2}',
            f'--layer-size-3 {layer_sizes_3}',
            f'--n-embedding {n_embedding}',
            f'--learning-rate {learning_rate}',
        ])
    ]    

    client.containers.run(image = image_name, device_requests = device_requests,
                        command = ' '.join(cli_command), 
                        volumes = volumes, ipc_mode = 'host',
                        stdin_open = True, tty = True, remove = True, detach = False)   

wide_deep_run()