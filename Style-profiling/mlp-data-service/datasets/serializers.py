import datetime

from rest_framework import serializers
from .models import Dataset
from annotations.models import Annotation

class DatasetSerializer(serializers.ModelSerializer):
    labeled_data = serializers.SerializerMethodField()
    total_data = serializers.SerializerMethodField()
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Dataset
        fields = '__all__'

    def get_labeled_data(self, obj):
        return Annotation.objects.filter(dataset_id=obj._id, done=1).exclude(labels=[]).count()
    
    def get_total_data(self, obj):
        return Annotation.objects.filter(dataset_id=obj._id).count()

class DatasetCreateDtoSerializer(serializers.Serializer):
    ml_task = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)

    def create(self, data):
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'user_id'

        return Dataset.objects.create(
            **data, 
            cover_image="",
            max_index = 0,
            # 표준 필드
            history={},
            ext={},
            reg_date=current_dt,
            reg_id=current_user_id,
            mod_date=current_dt,
            mod_id=current_user_id,
        )

class DatasetUpdateDtoSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    cover_image = serializers.CharField(required=False, allow_blank=True)