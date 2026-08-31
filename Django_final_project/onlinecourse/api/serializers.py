from rest_framework import serializers
from course.models import Course ,Category
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
class CourseSerializer2(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'