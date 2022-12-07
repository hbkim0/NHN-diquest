import datetime

from rest_framework import serializers
from .models import Label


class LabelSerializer(serializers.ModelSerializer):
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Label
        fields = '__all__'


class LabelCreateDtoSerializer(serializers.Serializer):
    dataset_id = serializers.CharField()
    name = serializers.CharField()
    color = serializers.CharField()


    def create(self, data):
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'user_id'

        return Label.objects.create(
            **data, 
            # 표준 필드
            history={},
            ext={},
            reg_date=current_dt,
            reg_id=current_user_id,
            mod_date=current_dt,
            mod_id=current_user_id,
        )


class LabelUpdateDtoSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    color = serializers.CharField(required=False, allow_blank=True)