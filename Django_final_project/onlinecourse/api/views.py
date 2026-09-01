from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from course.models import Course,Category
from .serializers import CourseSerializer,CategorySerializer,CourseSerializer2

from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsInstructorOrReadOnly

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated,IsInstructorOrReadOnly])
def  course_list_api(request):
     if request.method=='GET':
       courses= Course.objects.all()
       serialiser= CourseSerializer(courses, many=True)
       return Response(serialiser.data)
     if request.method=='POST':
        serializer=CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(instructor=request.user)
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

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
   