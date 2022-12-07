import datetime
import urllib.parse
import bson
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from misc.response import *
from misc import query_string

from .serializers import ModelSerializer
from .models import Model


class ModelList(APIView):
    filter_keys = []
    sortable_keys = [f.attname for f in Model._meta.concrete_fields]

    def get(self, request):
        try:
            filter_map, offset, limit, sort_by = query_string.parse(request.query_params, self.filter_keys, self.sortable_keys)
        except query_string.QSParsingFilterError:
            return ResponseError400BadRequest(0, f'filter parsing error: query_params={request.query_params}')
        except query_string.QSParsingPaginationError:
            return ResponseError400BadRequest(0, f'pagination parsing error: query_params={request.query_params}')
        except query_string.QSParsingSortingError:
            return ResponseError400BadRequest(0, f'sorting parsing error: query_params={request.query_params}')

        queryset = Model.objects.all()

        if len(sort_by):
            queryset = queryset.order_by(*sort_by)

        return ResponseList(
            queryset.count(),
            ModelSerializer(queryset[offset:(offset+limit)], many=True).data,
            limit=limit,
            offset=offset,
            sort_by=','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )