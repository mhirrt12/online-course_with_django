from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from course.models import Course,Category
from .serializers import CourseSerializer,CategorySerializer,CourseSerializer2

@api_view(['GET'])
def  course_list_api(request):
    courses= Course.objects.all()
    serialiser= CourseSerializer(courses, many=True)
    return Response(serialiser.data)

@api_view(['GET'])
def category_list_api(request):
    category= Category.objects.all()
    serializer=CategorySerializer(category, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def one_course(request):
    course= Course.objects.first()
    serializer= CourseSerializer2(course)
    return Response(serializer.data)