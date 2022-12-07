import datetime
import urllib.parse
import bson
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.views import APIView
import requests
import json 

from misc.response import *
from misc import query_string

from .serializers import ExperimentSerializer, ExperimentCreateDtoSerializer, ExperimentUpdateDtoSerializer
from .models import Experiment
from models.models import Model

from rp_data_service.settings import MLFLOW_URL


class ExperimentList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'seq_num_major': int,
        'seq_num_minor': int,
        'status': int,
        'model_id': str,
        'start': str,
        'end': str,
        'serving': int,
    })
    sortable_keys = [f.attname for f in Experiment._meta.concrete_fields]

    def post(self, request):
        try:
            model_id = request.data.get('model_id')
            Model.objects.get(_id=bson.ObjectId(model_id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'model not found: model_id={model_id}')
        except bson.errors.InvalidId:
            return ResponseError400BadRequest(0, f'invalid parameter: model_id={model_id}')

        serializer = ExperimentCreateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        result = serializer.save()
        return ResponseItemCreated(
            ExperimentSerializer(result).data,
            location=urllib.parse.urljoin(
                f'{request.build_absolute_uri()}/', f'{result._id}'
            )
        )

    def get(self, request):
        try:
            filter_map, offset, limit, sort_by = query_string.parse(request.query_params, self.filter_keys, self.sortable_keys)
        except query_string.QSParsingFilterError:
            return ResponseError400BadRequest(0, f'filter parsing error: query_params={request.query_params}')
        except query_string.QSParsingPaginationError:
            return ResponseError400BadRequest(0, f'pagination parsing error: query_params={request.query_params}')
        except query_string.QSParsingSortingError:
            return ResponseError400BadRequest(0, f'sorting parsing error: query_params={request.query_params}')

        start = request.query_params.get('start')
        end = request.query_params.get('end')
        
        queryset = Experiment.objects.all()

        if len(filter_map):
            filter_map_copy = filter_map.copy()
            try:
                if start:
                    queryset = queryset.filter(start_time__gte=start)
                    filter_map_copy.pop('start')
                if end:
                    queryset = queryset.filter(start_time__lte=end)
                    filter_map_copy.pop('end')
            except ValidationError:
                return ResponseError400BadRequest(0, f'invalid date format: query_params={request.query_params}')
            queryset = queryset.filter(**filter_map_copy)
        if len(sort_by):
            queryset = queryset.order_by(*sort_by)

        return ResponseList(
            queryset.count(),
            ExperimentSerializer(queryset[offset:(offset+limit)], many=True).data,
            limit=limit,
            offset=offset,
            sort_by=','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )

class ExperimentDetail(APIView):
    def get(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')
        
        try:
            item = Experiment.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(ExperimentSerializer(item).data)

    def patch(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        serializer = ExperimentUpdateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        additional_fields = {
            'mod_date': datetime.datetime.utcnow(),
            'mod_id': 'user_id',
        }

        modified_count = Experiment.objects.filter(_id=bson.ObjectId(id)).update(
            **serializer.data, 
            **additional_fields
        )
        if modified_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        try:
            item = Experiment.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        if item.serving == 2:
            try:
                response = requests.get(f'{MLFLOW_URL}api/2.0/mlflow/model-versions/search?filter=tags.exp_id%3D%27{str(item._id)}%27')
                response = response.json()
                model_info = response['model_versions'].pop()
                model_name = model_info['name']
                version = model_info['version']

                response = requests.post(f'{MLFLOW_URL}api/2.0/mlflow/model-versions/transition-stage', data = json.dumps({'name': model_name, 'version': version, 'stage': 'Production', 'archive_existing_versions': True}))

                Experiment.objects.filter(serving=2).exclude(_id=item._id).update(serving=0)
            except:
                item.serving = 0
                item.save()
                return ResponseError500InternalServerError(0, f'error transition-stage {str(item._id)}')
        else:
            pass

        return ResponseItem(ExperimentSerializer(item).data)

    def delete(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        deleted_count, _ = Experiment.objects.filter(_id=bson.ObjectId(id)).delete()
        if deleted_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItemDeleted()