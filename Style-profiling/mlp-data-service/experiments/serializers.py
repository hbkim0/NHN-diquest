import datetime
import bson
import json

from rest_framework import serializers
from .models import Experiment
from datasets.models import Dataset
from versioned_datasets.models import VersionedDataset
from models.models import Model

class ExperimentSerializer(serializers.ModelSerializer):
    algorithms = serializers.JSONField()
    artifacts = serializers.JSONField()
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Experiment
        fields = '__all__'
    
    def to_representation(self, instance):
        res = super().to_representation(instance)
        dataset = Dataset.objects.get(_id=bson.ObjectId(instance.dataset_id))
        versioned_dataset = VersionedDataset.objects.get(_id=bson.ObjectId(instance.versioned_dataset_id))
        model = Model.objects.get(_id=bson.ObjectId(instance.model_id))
        res.update({
            'ml_task': dataset.ml_task,
            'dataset_name': dataset.name,
            'versioned_dataset_name': versioned_dataset.name,
            'versioned_dataset_index': versioned_dataset.index,
            'model_name': model.name,
        })
        return res


class ExperimentCreateDtoSerializer(serializers.Serializer):
    dataset_id = serializers.CharField()
    versioned_dataset_id = serializers.CharField()
    model_id = serializers.CharField()
    name = serializers.CharField()

    def create(self, data):
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'user_id'
        algorithms = Model.objects.get(_id=bson.ObjectId(data['model_id'])).algorithms
        for item in algorithms:
            item.pop("image_name")
            for param in item['training_params']:
                param.update({ "argument": param.get('default', '')})
            for metric in item['performance_metrics']:
                metric.update({ "value": ""})

        return Experiment.objects.create(
            **data,
            description="",
            algorithms=algorithms,
            artifacts=[],
            status=0,
            # 표준 필드
            history={},
            ext={},
            reg_date=current_dt,
            reg_id=current_user_id,
            mod_date=current_dt,
            mod_id=current_user_id,
        )

class ExperimentUpdateDtoSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    algorithms = serializers.ListField(required=False)
    status = serializers.IntegerField(required=False)