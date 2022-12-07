from django.conf import settings

from rest_framework.views import APIView

from misc.response import *
from misc.utils import SearchModel, RecognitionModel


class Version(APIView):
    def get(self, request):
        if not 1:
            return ResponseError500InternalServerError(0, 'internal server error')

        version_dict = {
            'search_model': SearchModel().get_version(),
            'recognition_model': RecognitionModel().get_version(),
            'scroing_service': settings.SERVICE_VERSION,
        }
        return ResponseItem(version_dict)
