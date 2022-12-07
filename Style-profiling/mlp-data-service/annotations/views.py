import datetime
import urllib.parse
import bson
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from annotations.models import Annotation

from misc.response import *
from misc import query_string

from .serializers import AnnotationSerializer, AnnotationUpdateDtoSerializer
from .models import Annotation
from bundles.models import Bundle

class AnnotationList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'dataset_id': str,
        'bundle_id': str,
        'labeled': int,
        'versioned_dataset_id': str,
        'attribute': str,
        'split': int,
    })
    sortable_keys = [f.attname for f in Annotation._meta.concrete_fields]

    def get(self, request):
        try:
            filter_map, offset, limit, sort_by = query_string.parse(request.query_params, self.filter_keys, self.sortable_keys)
        except query_string.QSParsingFilterError:
            return ResponseError400BadRequest(0, f'filter parsing error: query_params={request.query_params}')
        except query_string.QSParsingPaginationError:
            return ResponseError400BadRequest(0, f'pagination parsing error: query_params={request.query_params}')
        except query_string.QSParsingSortingError:
            return ResponseError400BadRequest(0, f'sorting parsing error: query_params={request.query_params}')

        queryset = Annotation.objects.all()

        if len(filter_map):
            filter_map_copy = filter_map.copy()
            if 'labeled' or 'attribute' in filter_map:
                if 'labeled' in filter_map:
                    if filter_map['labeled'] == 1:
                        queryset = queryset.exclude(labels=[]).exclude(done=0)
                    elif filter_map['labeled'] == 0:
                        queryset = queryset.filter(labels=[], done=0)
                    filter_map_copy.pop('labeled')
                if 'attribute' in filter_map:
                    key, value = filter_map['attribute'].split(":")[0], filter_map['attribute'].split(":")[1]
                    bundle_lists = list(Bundle.objects.filter(attributes={'key': key, 'values': value}).values_list('_id', flat=True))
                    bundle_ids = [str(objectid) for objectid in bundle_lists]
                    queryset = Annotation.objects.filter(bundle_id__in=bundle_ids)
                    filter_map_copy.pop('attribute')
            if 'bundle_id' in request.query_params:
                queryset = queryset.filter(bundle_id__in=request.query_params.getlist('bundle_id'))
                filter_map_copy.pop('bundle_id')
                
            queryset = queryset.filter(**filter_map_copy)
        else:
            queryset = queryset.filter(**filter_map)
        if len(sort_by):
            queryset = queryset.order_by(*sort_by)
                
        return ResponseList(
            queryset.count(),
            AnnotationSerializer(queryset[offset:(offset+limit)], many=True).data,
            limit=limit,
            offset=offset,
            sort_by=','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )
        

class AnnotationDetail(APIView):
    def get(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')
        
        try:
            item = Annotation.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(AnnotationSerializer(item).data)
        
    def patch(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        serializer = AnnotationUpdateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        additional_fields = {
            'mod_date': datetime.datetime.utcnow(),
            'mod_id': 'user_id',
        }

        modified_count = Annotation.objects.filter(_id=bson.ObjectId(id)).update(
            **serializer.data, 
            **additional_fields
        )
        if modified_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        try:
            item = Annotation.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(AnnotationSerializer(item).data)