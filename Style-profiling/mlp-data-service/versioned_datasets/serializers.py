import datetime
import bson

from rest_framework import serializers
from datasets.models import Dataset

from .models import VersionedDataset
from datasets.models import Dataset
from bundles.models import Bundle

class VersionedDatasetSerializer(serializers.ModelSerializer):
    ml_task = serializers.SerializerMethodField() 
    dataset_name = serializers.SerializerMethodField()
    preprocessing = serializers.JSONField()
    augmentation = serializers.JSONField()
    bundle_ids = serializers.JSONField()
    attribute_info = serializers.ListField()

    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = VersionedDataset
        fields = '__all__' 

    def get_ml_task(self, obj):
        return Dataset.objects.get(_id=bson.ObjectId(obj.dataset_id)).ml_task

    def get_dataset_name(self, obj):
        return Dataset.objects.get(_id=bson.ObjectId(obj.dataset_id)).name

class VersionedDatasetCreateDto(serializers.Serializer):
    dataset_id = serializers.CharField()
    bundle_ids = serializers.JSONField()
    split = serializers.JSONField()
    preprocessing = serializers.JSONField()
    augmentation = serializers.JSONField()
    name = serializers.CharField()
    
    def create(self, data):
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'user_id'
        attributes_list = Bundle.objects.filter(_id__in=[bson.ObjectId(x) for x in data['bundle_ids']]).values_list('attributes', flat = True)
        attribute_info = []
        attribute_keys = []
        for attributes in attributes_list:
            for item in attributes:
                if not item['key'] in attribute_keys:
                    attribute_keys.append(item['key'])
                    attribute_info.append({ 'key': item['key'], 'values': item['values']})
                else:
                    attribute_info[attribute_keys.index(item['key'])]['values'].extend(item['values'])

        return VersionedDataset.objects.create(
            **data,
            status=0,
            index=Dataset.objects.get(_id=bson.ObjectId(data['dataset_id'])).max_index+1,
            attribute_info=attribute_info,
            # 표준 필드
            history={},
            ext={},
            reg_date=current_dt,
            reg_id=current_user_id,
            mod_date=current_dt,
            mod_id=current_user_id,
        )

class VersionedDatasetUpdateDtoSerializer(serializers.Serializer):
    status = serializers.IntegerField(required=True)