import datetime

from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = File
        fields = '__all__'

class FileUploadSerializer(serializers.Serializer):
    dataset_id = serializers.CharField()
    bundle_id = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField()
    url = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)

    def create(self, data):
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'user_id'

        return File.objects.create(
            **data,
            # 표준 필드
            history={},
            ext={},
            reg_date=current_dt,
            reg_id=current_user_id,
            mod_date=current_dt,
            mod_id=current_user_id,
        )