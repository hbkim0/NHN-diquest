import datetime
import urllib.parse
import bson
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from misc.response import *
from misc import query_string

from .serializers import LabelSerializer, LabelCreateDtoSerializer, LabelUpdateDtoSerializer
from .models import Label


class LabelList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'dataset_id': str,
    })
    sortable_keys = [f.attname for f in Label._meta.concrete_fields]

    def post(self, request):
        serializer = LabelCreateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        result = serializer.save()
        return ResponseItemCreated(
            LabelSerializer(result).data,
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

        queryset = Label.objects.all()

        if len(filter_map):
            queryset = queryset.filter(**filter_map)
        if len(sort_by):
            queryset = queryset.order_by(*sort_by)

        return ResponseList(
            queryset.count(),
            LabelSerializer(queryset[offset:(offset+limit)], many=True).data,
            limit=limit,
            offset=offset,
            sort_by=','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )
        

class LabelDetail(APIView):
    def get(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')
        
        try:
            item = Label.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(LabelSerializer(item).data)
        
    def patch(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        serializer = LabelUpdateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        additional_fields = {
            'mod_date': datetime.datetime.utcnow(),
            'mod_id': 'user_id',
        }

        modified_count = Label.objects.filter(_id=bson.ObjectId(id)).update(
            **serializer.data, 
            **additional_fields
        )
        if modified_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        try:
            item = Label.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(LabelSerializer(item).data)