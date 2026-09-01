from django.shortcuts import render, get_object_or_404
# Create your views here.
from rest_framework.response import Response
from course.models import Course,Category
from .serializers import CourseSerializer,CategorySerializer,CourseSerializer2
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsInstructorOrReadOnly
from rest_framework.views import APIView
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
class CourseDetailAPIView(APIView):

    def get(self, request, id):
       course = get_object_or_404(Course,id=id)
       self.check_object_permissions(request, course)
       serializer=CourseSerializer(course)
       return Response(serializer.data)

    def put(self, request, id):
        course=get_object_or_404(Course , id=id)
        self.check_object_permissions(request, course)
        serializer=CourseSerializer(course,data=request.data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        course= get_object_or_404(Course,id=id)
        self.check_object_permissions(request, course)
        course.delete()
        return Response (status =204 )