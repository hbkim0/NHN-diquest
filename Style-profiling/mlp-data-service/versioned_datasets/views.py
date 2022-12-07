import bson
import urllib.parse

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from misc.response import *
from misc import query_string

from .models import VersionedDataset
from .serializers import VersionedDatasetCreateDto, VersionedDatasetSerializer
from .tasks import generate_versioned_dataset
from datasets.models import Dataset
from annotations.models import Annotation
from files.models import File
from experiments.models import Experiment


class VersionedDatasetList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'ml_task': int,  
        'dataset_id': str,
        'status': int,
    })
    sortable_keys = [f.attname for f in VersionedDataset._meta.concrete_fields]

    def post(self, request):
        serializer = VersionedDatasetCreateDto(data=request.data) 

        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        result = serializer.save()
        Dataset.objects.filter(_id=bson.ObjectId(request.data['dataset_id'])).update(max_index=result.index+1)
        
        serialized_data = VersionedDatasetSerializer(result).data
        generate_versioned_dataset(serialized_data)
        
        return ResponseItemCreated(
            serialized_data,
            location = urllib.parse.urljoin(
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

        queryset = VersionedDataset.objects.all()

        if len(filter_map): 
            if 'ml_task' in filter_map:
                dataset_list = list(Dataset.objects.filter(ml_task=bson.Int64(filter_map['ml_task'])).values_list('_id', flat=True))
                str_dataset_list = [str(objectid) for objectid in dataset_list] 
                queryset = VersionedDataset.objects.filter(dataset_id__in=str_dataset_list)

                filter_map_copy = filter_map.copy()
                filter_map_copy.pop('ml_task')

                queryset = queryset.filter(**filter_map_copy)
            else:
                queryset = queryset.filter(**filter_map)

        if len(sort_by):
            queryset = queryset.order_by(*sort_by)

        return ResponseList(
            queryset.count(),
            VersionedDatasetSerializer(queryset[offset:(offset+limit)], many=True).data,
            limit = limit,
            offset = offset,
            sort_by = ','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )


class VersionedDatasetDetail(APIView):
    def get(self, request, id): 
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')
        
        try:
            item = VersionedDataset.objects.get(_id = bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')
        
        return ResponseItem(VersionedDatasetSerializer(item).data)

    def delete(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        Annotation.objects.filter(versioned_dataset_id=id).delete()
        File.objects.filter(versioned_dataset_id=id).delete()
        Experiment.objects.filter(versioned_dataset_id=id).delete()

        deleted_count, _ = VersionedDataset.objects.filter(_id=bson.ObjectId(id)).delete()
        if deleted_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItemDeleted()