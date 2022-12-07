import urllib.parse
import bson
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from misc.response import *
from misc import query_string

from .serializers import ScheduleSerializer, ScheduleCreateDtoSerializer, ScheduleUpdateDtoSerializer
from .models import Schedule
from .tasks import duplicate_experiments


class ScheduleList(APIView):
    def post(self, request):
        try:
            item = Schedule.objects.get(priority=1)
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'schedule not found')
        duplicate_experiments(item)

        return ResponseOK({ 'message': 'Successfully invoked.'})

    def get(self, request):
        try:
            item = Schedule.objects.get(priority=1)
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'schedule not found')

        return ResponseItem(ScheduleSerializer(item).data)

    def patch(self, request):
        serializer = ScheduleUpdateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        modified_count = Schedule.objects.filter(priority=1).update(**serializer.data)
        if modified_count < 1:
            return ResponseError404NotFound(0, f'schedule not found')

        try:
            item = Schedule.objects.get(priority=1)
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'schedule not found')

        return ResponseItem(ScheduleSerializer(item).data)