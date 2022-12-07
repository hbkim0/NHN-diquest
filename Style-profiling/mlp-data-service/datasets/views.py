import datetime
import urllib.parse
import bson
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from annotations.models import Annotation
from bundles.models import Bundle
from labels.models import Label
from versioned_datasets.models import VersionedDataset
from experiments.models import Experiment

from misc.response import *
from misc import query_string

from .serializers import DatasetSerializer, DatasetCreateDtoSerializer, DatasetUpdateDtoSerializer
from .models import Dataset
from bundles.serializers import BundleCreateDtoSerializer


class DatasetList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'ml_task': int,
    })
    sortable_keys = [f.attname for f in Dataset._meta.concrete_fields]

    def post(self, request):
        serializer = DatasetCreateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        result = serializer.save()
        bundle_data = {
            'dataset_id': str(result._id),
            'name': 'default',
            'description': ''
        }
        bundle = BundleCreateDtoSerializer(data=bundle_data)
        if not bundle.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={bundle_data}')
        bundle.save()

        return ResponseItemCreated(
            DatasetSerializer(result).data,
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

        queryset = Dataset.objects.all()

        if len(filter_map):
            queryset = queryset.filter(**filter_map)
        if len(sort_by):
            queryset = queryset.order_by(*sort_by)

        return ResponseList(
            queryset.count(),
            DatasetSerializer(queryset[offset:(offset+limit)], many=True).data,
            limit=limit,
            offset=offset,
            sort_by=','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )
        

class DatasetDetail(APIView):
    def get(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')
        
        try:
            item = Dataset.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(DatasetSerializer(item).data)
        
    def patch(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        serializer = DatasetUpdateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        additional_fields = {
            'mod_date': datetime.datetime.utcnow(),
            'mod_id': 'user_id',
        }

        modified_count = Dataset.objects.filter(_id=bson.ObjectId(id)).update(
            **serializer.data, 
            **additional_fields
        )
        if modified_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        try:
            item = Dataset.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(DatasetSerializer(item).data)

    def delete(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        Bundle.objects.filter(dataset_id=id).delete()
        Annotation.objects.filter(dataset_id=id).delete()
        Label.objects.filter(dataset_id=id).delete()
        VersionedDataset.objects.filter(dataset_id=id).delete()
        Experiment.objects.filter(dataset_id=id).delete()

        deleted_count, _ = Dataset.objects.filter(_id=bson.ObjectId(id)).delete()
        if deleted_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItemDeleted()