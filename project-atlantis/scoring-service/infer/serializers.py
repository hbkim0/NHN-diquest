from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Log

import fastjsonschema


_VALIDATE = fastjsonschema.compile(
    {
        "type": "array", 
        "minItems": 1, 
        "items": {
            "type": "object", 
            "required": ["prob_num", "answers"], 
            "properties": {
                "prob_num": {"type": "string"}, 
                "answers": {
                    "type": "array", 
                    "minItems": 1, 
                    "items": {"type": "string"}
                }
            }
        }
    }
)


def _validate_predictions(predictions):
    try:
        _VALIDATE(predictions)
    except fastjsonschema.JsonSchemaException:
        raise ValidationError()

    return predictions


class DnRRequestSerializer(serializers.Serializer):
    input_url = serializers.CharField()
    log = serializers.IntegerField(required=False, default=1)
    user_id = serializers.CharField(required=False, allow_null=True)


class ScoreRequestSerializer(serializers.Serializer):
    page_id = serializers.CharField()
    predictions = serializers.JSONField(validators=[_validate_predictions, ])
    log_id = serializers.CharField(required=False, allow_null=True)
    user_id = serializers.CharField(required=False, allow_null=True)


class LogSerializer(serializers.ModelSerializer):
    workbook = serializers.JSONField()
    page = serializers.JSONField()
    scoring = serializers.JSONField()  # validatiors ------------------------------------------
    user_id = serializers.CharField()

    class Meta:
        model = Log
        fields = '__all__'


# class LogUpdateDtoSerializer(serializers.Serializer):
    # custom_answer = serializers.JSONField(required=False)
    # correct = serializers.JSONField()