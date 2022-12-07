import bson
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from misc.response import *
from .serializers import StudentSerializer
from .models import Student

@permission_classes([IsAuthenticated])
class StudentDetail(APIView):

    def get(self, request, id):
        # path parameter(s)
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        #
        try:
            item = Student.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        if not item.user_id == request.user.username:
            return ResponseError(0, f'no permissions.', HTTP_403_FORBIDDEN) 

        #
        return ResponseItem(StudentSerializer(item).data)