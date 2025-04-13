from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['username', 'email', 'phone', 'course', 'cgpa', 'password']

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
