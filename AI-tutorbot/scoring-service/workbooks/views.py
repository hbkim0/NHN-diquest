import datetime
import urllib.parse
import bson
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from misc.response import *
from misc import query_string

from .serializers import WorkbookSerializer, WorkbookCreateDtoSerializer, WorkbookUpdateDtoSerializer
from .models import Workbook
from pages.models import Page


class WorkbookList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'name': str,
        'valid': int,
        'applied': int,
    })
    sortable_keys = [f.attname for f in Workbook._meta.concrete_fields]

    def post(self, request):
        serializer = WorkbookCreateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        result = serializer.save()
        return ResponseItemCreated(
            WorkbookSerializer(result).data,
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

        queryset = Workbook.objects.all()

        if len(filter_map):
            queryset = queryset.filter(**filter_map)
        if len(sort_by):
            queryset = queryset.order_by(*sort_by)

        return ResponseList(
            queryset.count(),
            WorkbookSerializer(queryset[offset:(offset+limit)], many=True).data,
            limit=limit,
            offset=offset,
            sort_by=','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )
        

class WorkbookDetail(APIView):
    def get(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')
        
        try:
            item = Workbook.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(WorkbookSerializer(item).data)
        
    def patch(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        serializer = WorkbookUpdateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        additional_fields = {
            'mod_date': datetime.datetime.utcnow(),
            'mod_id': 'user_id',
        }

        modified_count = Workbook.objects.filter(_id=bson.ObjectId(id)).update(
            **serializer.data, 
            **additional_fields
        )
        if modified_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        try:
            item = Workbook.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(WorkbookSerializer(item).data)

    def delete(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        Page.objects.filter(workbook_id=id).delete()
        deleted_count, _ = Workbook.objects.filter(_id=bson.ObjectId(id)).delete()
        if deleted_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItemDeleted()