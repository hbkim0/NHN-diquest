import datetime

from rest_framework import serializers
from .models import Workbook


class WorkbookSerializer(serializers.ModelSerializer):
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Workbook
        fields = '__all__'


class WorkbookCreateDtoSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)

    def create(self, data):
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'user_id'

        return Workbook.objects.create(
            **data, 
            no_pages=0, 
            valid=0, 
            applied=0, 
            # 표준 필드
            history={},
            ext={},
            reg_date=current_dt,
            reg_id=current_user_id,
            mod_date=current_dt,
            mod_id=current_user_id,
        )


class WorkbookUpdateDtoSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    image_url = serializers.CharField(required=False, allow_blank=True)
    applied = serializers.IntegerField(required=False)
