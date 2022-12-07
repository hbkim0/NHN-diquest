from rest_framework import serializers
from .models import Model

class ModelSerializer(serializers.ModelSerializer):
    parameters = serializers.JSONField()
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Model
        fields = '__all__'