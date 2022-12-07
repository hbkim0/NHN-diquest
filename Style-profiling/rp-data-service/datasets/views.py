import bson
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.views import APIView

from misc.response import *
from misc import query_string

from .serializers import DatasetStatusSerializer, DatasetCustomerSerializer, DatasetProductSerializer, DatasetHistorySerializer
from .models import Status, Customer, Product, History


class DatasetStatusList(APIView):
    def get(self, request):
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        
        queryset = Status.objects.all()

        try:
            if start:
                queryset = queryset.filter(date__gte=start)
            if end:
                queryset = queryset.filter(date__lte=end)
        except ValidationError:
            return ResponseError400BadRequest(0, f'invalid date format: query_params={request.query_params}')

        return ResponseOK(DatasetStatusSerializer(queryset, many=True).data)

class DatasetCustomerList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'identifier': int,
        'gender': str,
    })
    sortable_keys = [f.attname for f in Customer._meta.concrete_fields]

    def get(self, request):
        try:
            filter_map, offset, limit, sort_by = query_string.parse(request.query_params, self.filter_keys, self.sortable_keys)
        except query_string.QSParsingFilterError:
            return ResponseError400BadRequest(0, f'filter parsing error: query_params={request.query_params}')
        except query_string.QSParsingPaginationError:
            return ResponseError400BadRequest(0, f'pagination parsing error: query_params={request.query_params}')
        except query_string.QSParsingSortingError:
            return ResponseError400BadRequest(0, f'sorting parsing error: query_params={request.query_params}')

        queryset = Customer.objects.all()

        if len(filter_map):
            queryset = queryset.filter(**filter_map)
        if len(sort_by):
            queryset = queryset.order_by(*sort_by)

        return ResponseList(
            queryset.count(),
            DatasetCustomerSerializer(queryset[offset:(offset+limit)], many=True).data,
            limit=limit,
            offset=offset,
            sort_by=','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )

class DatasetProductList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'identifier': int,
        'label': str,
        'gender': str,
        'name': str,
    })
    sortable_keys = [f.attname for f in Product._meta.concrete_fields]

    def get(self, request):
        try:
            filter_map, offset, limit, sort_by = query_string.parse(request.query_params, self.filter_keys, self.sortable_keys)
        except query_string.QSParsingFilterError:
            return ResponseError400BadRequest(0, f'filter parsing error: query_params={request.query_params}')
        except query_string.QSParsingPaginationError:
            return ResponseError400BadRequest(0, f'pagination parsing error: query_params={request.query_params}')
        except query_string.QSParsingSortingError:
            return ResponseError400BadRequest(0, f'sorting parsing error: query_params={request.query_params}')

        queryset = Product.objects.all()

        if len(filter_map):
            queryset = queryset.filter(**filter_map)
        if len(sort_by):
            queryset = queryset.order_by(*sort_by)

        return ResponseListExtraInfo(
            queryset.count(),
            DatasetProductSerializer(queryset[offset:(offset+limit)], many=True).data,
            info=queryset.values_list('label', flat=True).distinct().order_by(),
            limit=limit,
            offset=offset,
            sort_by=','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )

class DatasetProductAutocomplete(APIView):
    def get(self, request):
        q = request.query_params.get('q')
        if not q:
            return ResponseOK([])

        return ResponseOK(list(Product.objects.filter(name__istartswith=q).values_list('name', flat=True))[:10])

class DatasetProductDetail(APIView):
    def get(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')
        
        try:
            item = Product.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(DatasetProductSerializer(item).data)

class DatasetHistoryList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'customer': int,
        'product': int,
        'start': str,
        'end': str,
    })
    sortable_keys = [f.attname for f in History._meta.concrete_fields]

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

        queryset = History.objects.all()

        if len(filter_map):
            filter_map_copy = filter_map.copy()
            try:
                if start:
                    queryset = queryset.filter(reg_date__gte=start)
                    filter_map_copy.pop('start')
                if end:
                    queryset = queryset.filter(reg_date__lte=end)
                    filter_map_copy.pop('end')
            except ValidationError:
                return ResponseError400BadRequest(0, f'invalid date format: query_params={request.query_params}')
            queryset = queryset.filter(**filter_map_copy)
        if len(sort_by):
            queryset = queryset.order_by(*sort_by)

        return ResponseList(
            queryset.count(),
            DatasetHistorySerializer(queryset[offset:(offset+limit)], many=True).data,
            limit=limit,
            offset=offset,
            sort_by=','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )