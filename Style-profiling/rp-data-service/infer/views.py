import bson
from random import choice
from rest_framework.views import APIView

from misc.response import *

from datasets.models import Product

class InferText(APIView):
    def post(self, request):
        pick = choice(Product.objects.values_list('identifier', flat=True))
        return ResponseOK(Product.objects.get(identifier=pick).attributes)

class InferImage(APIView):
    def post(self, request):
        pick = choice(Product.objects.values_list('identifier', flat=True))
        return ResponseOK(Product.objects.get(identifier=pick).attributes)