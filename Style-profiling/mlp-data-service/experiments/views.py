import datetime
import urllib.parse
import bson
from rest_framework.views import APIView

from misc.response import *
from misc import query_string

from .serializers import ExperimentSerializer, ExperimentCreateDtoSerializer, ExperimentUpdateDtoSerializer
from .models import Experiment
from datasets.models import Dataset


class ExperimentList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'ml_task': int,
        'dataset_id': str,
        'status': int,
    })
    sortable_keys = [f.attname for f in Experiment._meta.concrete_fields]

    def post(self, request):
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

        queryset = Experiment.objects.all()

        if len(filter_map): 
            if 'ml_task' in filter_map:
                dataset_list = list(Dataset.objects.filter(ml_task=bson.Int64(filter_map['ml_task'])).values_list('_id', flat=True))
                str_dataset_list = [str(objectid) for objectid in dataset_list] 
                queryset = Experiment.objects.filter(dataset_id__in=str_dataset_list)

                filter_map_copy = filter_map.copy()
                filter_map_copy.pop('ml_task')

                queryset = queryset.filter(**filter_map_copy)
            else:
                queryset = queryset.filter(**filter_map)
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

        return ResponseItem(ExperimentSerializer(item).data)

    def delete(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        try:
            item = Experiment.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        if not item.status in [0, 3, 4]:
            return ResponseError400BadRequest(0, f'invalid status: status={item.status}')

        deleted_count, _ = Experiment.objects.filter(_id=bson.ObjectId(id)).delete()
        if deleted_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItemDeleted()