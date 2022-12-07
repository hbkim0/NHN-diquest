import datetime

from rest_framework import serializers
from .models import Experiment

class ExperimentSerializer(serializers.ModelSerializer):
    parameters = serializers.JSONField()
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Experiment
        fields = '__all__'

class ExperimentCreateDtoSerializer(serializers.Serializer):
    model_id = serializers.CharField()
    parameters = serializers.JSONField()

    def create(self, data):
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'user_id'

        return Experiment.objects.create(
            **data,
            seq_num_major=None,
            seq_num_minor=None,
            status=0,
            serving=0,
            start_time=None,
            end_time=None,
            rmse=None,
            # 표준 필드
            history={},
            ext={},
            reg_date=current_dt,
            reg_id=current_user_id,
            mod_date=current_dt,
            mod_id=current_user_id,
        )

class ExperimentUpdateDtoSerializer(serializers.Serializer):
    parameters = serializers.JSONField(required=False)
    serving = serializers.IntegerField(required=False)
