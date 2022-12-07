import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Page

import fastjsonschema
from .compiled_problems import validate


class PageSerializer(serializers.ModelSerializer):
    vector = serializers.JSONField()
    problems = serializers.JSONField()

    # 표준필드
    history = serializers.JSONField()
    ext = serializers.JSONField()
    
    class Meta:
        model = Page
        fields = '__all__'


def _validate_problems(problems):
    try:
        validate(problems)
    except fastjsonschema.JsonSchemaException:
        raise ValidationError()

    return problems


class PageCreateDtoSerializer(serializers.Serializer):
    workbook_id = serializers.CharField()
    page_num = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)

    def create(self, data):
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'user_id'

        return Page.objects.create(
            **data, 
            labeled=0, 
            vector=[], 
            problems=[],
            # 표준 필드
            history={},
            ext={},
            reg_date=current_dt,
            reg_id=current_user_id,
            mod_date=current_dt,
            mod_id=current_user_id,
        )


class PageUpdateDtoSerializer(serializers.Serializer):
    page_num = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    original_url = serializers.CharField(required=False, allow_blank=True)
    sample_url = serializers.CharField(required=False, allow_blank=True)
    problems = serializers.ListField(required=False, validators=[_validate_problems, ])
