import pathlib
import multiprocessing

import bson
import django.conf
import django.http.request
from rest_framework.views import APIView
from rest_framework.response import Response
import tensorboard

from misc.response import *
# from misc import query_string
from experiments.serializers import ExperimentSerializer
from experiments.models import Experiment
from .serializers import LaunchTensorboardSerializer


class TensorboardList(APIView):
    def get(self, request):
        serializer = ExperimentSerializer(Experiment.objects.all(), many = True)
        return Response(serializer.data)

    def post(self, request):

        # body parameter
        serializer = LaunchTensorboardSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        #
        experiment_ids = serializer.validated_data.get('experiment_ids')
        for experiment_id in experiment_ids:
            if not bson.ObjectId.is_valid(experiment_id):
                return ResponseError400BadRequest(0, f'invalid parameter: body.experiment_ids={experiment_ids}')
        experiment_ids = [bson.ObjectId(experiment_id) for experiment_id in experiment_ids]

        #
        queryset = Experiment.objects.filter(_id__in = experiment_ids)
        if queryset.count() == 0:
            return ResponseError404NotFound(0, f'not found experiments: body.experiment_ids={experiment_ids}')
        experiments = list(queryset)

        #
        logdir_spec = []
        for experiment in experiments:
            logdir_dict = experiment.artifacts.pop()
            logdir = logdir_dict['tensorboard_logdir']
            if len(logdir) == 0:
                continue

            logdir = pathlib.Path(django.conf.settings.TSBOARD_BASE_PATH, logdir).resolve()
            if not logdir.is_dir():
                continue

            logdir_spec.append(f'{str(experiment._id)}:{str(logdir.parent)}')

        if len(logdir_spec) == 0:
            return ResponseError404NotFound(0, f'not found summary: body.experiment_ids={experiment_ids}')

        #
        port = django.conf.settings.TSBOARD_DEFAULT_PORT
        launch_tensorboard(','.join(logdir_spec), port)

        #
        host = request.get_host()
        domain, _port = django.http.request.split_domain_port(host)
        tb_url = f'{request.scheme}://{domain}:{port}'

        return ResponseOK({'url': tb_url})


_tb_process: multiprocessing.Process = None
def launch_tensorboard(logdir_spec, port=None):
    global _tb_process

    if port is None:
        port = django.conf.settings.TSBOARD_DEFAULT_PORT

    #
    if _tb_process is not None:
        _tb_process.kill()
        _tb_process.join()
        _tb_process = None

    #
    tb_config = {
        'logdir_spec': logdir_spec,
        'port': port,
        'bind_all': True,

        # see : https://github.com/tensorflow/tensorboard/blob/2.8.0/tensorboard/backend/event_processing/data_ingester.py#L112
        # Only load the multiplexer once. Do not continuously reload.
        #
        # logdir_spec의 directory가 nfs로 연결된 경우, lock이 발생하는 것으로 추정됨.
        # training 중에 tensorboard를 띄울수 있다는 시나리오가 추가된다면, 이 옵션을 조정해야 할 필요가 있어 보임.
        'reload_interval': 0,
    }

    tb = tensorboard.program.TensorBoard()
    tb.configure(**tb_config)
    tb_process = multiprocessing.Process(target=tb.main)
    tb_process.start()

    #
    _tb_process = tb_process
