from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class ScheduleCreateDtoSerializer(serializers.Serializer):
    cron = serializers.CharField()
    priority = serializers.IntegerField()

    def create(self, data):
        return Schedule.objects.create(
            **data,
            sequence=1,
        )

class ScheduleUpdateDtoSerializer(serializers.Serializer):
    cron = serializers.CharField()