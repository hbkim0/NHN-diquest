import datetime

from rest_framework import serializers
from .models import Bundle
from annotations.models import Annotation


class BundleSerializer(serializers.ModelSerializer):
    labeled_data = serializers.SerializerMethodField()
    total_data = serializers.SerializerMethodField()
    attributes = serializers.JSONField()
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Bundle
        fields = '__all__'

    def get_labeled_data(self, obj):
        return Annotation.objects.filter(bundle_id=obj._id, dataset_id=obj.dataset_id, done=1).exclude(labels=[]).count()
    
    def get_total_data(self, obj):
        return Annotation.objects.filter(bundle_id=obj._id, dataset_id=obj.dataset_id).count()


class BundleCreateDtoSerializer(serializers.Serializer):
    dataset_id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)

    def create(self, data):
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'user_id'

        return Bundle.objects.create(
            **data, 
            attributes=[],
            # 표준 필드
            history={},
            ext={},
            reg_date=current_dt,
            reg_id=current_user_id,
            mod_date=current_dt,
            mod_id=current_user_id,
        )


class BundleUpdateDtoSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    attributes = serializers.ListField(required=False)