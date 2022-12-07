import datetime
import bson
import json

from rest_framework import serializers
from .models import Annotation
from datasets.models import Dataset
from files.models import File
from labels.models import Label
from bundles.models import Bundle
from versioned_datasets.models import VersionedDataset

class AnnotationSerializer(serializers.ModelSerializer):
    ml_task = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    label_info = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Annotation
        fields = '__all__'

    def get_ml_task(self, obj):
        if obj.dataset_id == '':
            dataset_id = Dataset.objects.get(_id=bson.ObjectId(
                VersionedDataset.objects.get(_id=bson.ObjectId(obj.versioned_dataset_id)).dataset_id))._id
        else:
            dataset_id = obj.dataset_id
        return Dataset.objects.get(_id=bson.ObjectId(dataset_id)).ml_task
    
    def get_file_name(self, obj):
        return File.objects.get(_id=bson.ObjectId(obj.file_id)).name

    def get_file_url(self, obj):
        return File.objects.get(_id=bson.ObjectId(obj.file_id)).url
    
    def get_label_info(self, obj):
        if obj.dataset_id == '':
            dataset_id = Dataset.objects.get(_id=bson.ObjectId(
                VersionedDataset.objects.get(_id=bson.ObjectId(obj.versioned_dataset_id)).dataset_id))._id
        else:
            dataset_id = obj.dataset_id
        return [dict({'label_id': str(item._id), 'name': item.name, 'color': item.color}) for item in Label.objects.filter(dataset_id=dataset_id)]

    def get_labels(self, obj):
        for item in obj.labels:
            if 'label_id' in item:
                label = Label.objects.get(_id=bson.ObjectId(item['label_id']))
                item.update({'label': label.name, 'color': label.color})
        return obj.labels


class AnnotationCreateDtoSerializer(serializers.Serializer):
    dataset_id = serializers.CharField()
    bundle_id = serializers.CharField()
    file_id = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)

    def create(self, data):
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'user_id'

        return Annotation.objects.create(
            **data,
            split=None,
            done=0,
            labels=[],
            # 표준 필드
            history={},
            ext={},
            reg_date=current_dt,
            reg_id=current_user_id,
            mod_date=current_dt,
            mod_id=current_user_id,
        )

class AnnotationVersionedCreateDtoSerializer(serializers.Serializer):
    versioned_dataset_id = serializers.CharField()
    file_id = serializers.CharField()
    split = serializers.IntegerField()
    description = serializers.CharField(required=False, allow_blank=True)

    def create(self, data):
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'user_id'

        return Annotation.objects.create(
            **data, 
            done=1,
            labels=[],
            # 표준 필드
            history={},
            ext={},
            reg_date=current_dt,
            reg_id=current_user_id,
            mod_date=current_dt,
            mod_id=current_user_id,
        )


class AnnotationUpdateDtoSerializer(serializers.Serializer):
    done = serializers.IntegerField(required=False)
    labels = serializers.ListField(required=False)