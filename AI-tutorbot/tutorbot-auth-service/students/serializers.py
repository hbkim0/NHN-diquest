from rest_framework import serializers

from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    pages_today = serializers.JSONField()
    pages_tomorrow = serializers.JSONField()
    
    # 표준필드
    history = serializers.JSONField()
    ext = serializers.JSONField()

    class Meta:
        model = Student
        fields = '__all__'