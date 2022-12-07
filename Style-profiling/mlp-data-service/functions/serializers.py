import datetime

from rest_framework import serializers
from .models import Function

class FunctionSerializer(serializers.ModelSerializer):
    params = serializers.JSONField()
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Function
        fields = '__all__'