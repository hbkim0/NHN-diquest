import bson

from rest_framework import serializers
from .models import Status, Customer, Product, History

class DatasetStatusSerializer(serializers.ModelSerializer):
    customer = serializers.JSONField()
    product = serializers.JSONField()
    history = serializers.JSONField()

    class Meta:
        model = Status
        fields = '__all__'

class DatasetCustomerSerializer(serializers.ModelSerializer):
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Customer
        fields = '__all__'

class DatasetProductSerializer(serializers.ModelSerializer):
    attributes = serializers.JSONField()
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Product
        fields = '__all__'

class DatasetHistorySerializer(serializers.ModelSerializer):
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = History
        fields = '__all__'