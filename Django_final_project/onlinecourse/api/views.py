from django.http import request
from django.shortcuts import render, get_object_or_404
# Create your views here.
from rest_framework.response import Response
from course.models import Course,Category
from .serializers import CourseSerializer,CategorySerializer,CourseSerializer2,UserSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.decorators import (api_view,permission_classes,action )
from rest_framework.permissions import IsAuthenticated
from .permissions import IsInstructorOrReadOnly
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate 
# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated,IsInstructorOrReadOnly])
# def  course_list_api(request):
#      if request.method=='GET':
#        courses= Course.objects.all()
#        serialiser= CourseSerializer(courses, many=True)
#        return Response(serialiser.data)
#      if request.method=='POST':
#         serializer=CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(instructor=request.user)
#             return Response(serializer.data,status=201)
#         return Response(serializer.errors,status=400)

# @api_view(['GET'])
# def category_list_api(request):
#     category= Category.objects.all()
#     serializer=CategorySerializer(category, many=True)
#     return Response(serializer.data)
# @api_view(['GET'])
# def one_course(request):
#        course= Course.objects.first()
#        serializer= CourseSerializer2(course)
#        return Response(serializer.data)
# class CourseDetailAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     permission_classes = [IsAuthenticated, IsInstructorOrReadOnly]
# class CourseListCreateAPIView(ListCreateAPIView):

#     queryset = Course.objects.all()

#     serializer_class = CourseSerializer

#     permission_classes = [
#         IsAuthenticated,
#         IsInstructorOrReadOnly
#     ]

#     def perform_create(self, serializer):
#         serializer.save(instructor=self.request.user)
from rest_framework.viewsets import ModelViewSet

@api_view(['POST'])
def login (request):
    username= request.data.get('username')
    password= request.data.get('password')
    user =authenticate(username=username,password=password)
    if user is None:
        return Response({"error":"Invalid username and password. "},
                        status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)
    return Response({"message":"Login successful. ", "token":token.key})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return Response(
        {"message": "Logout successful."},
        status=status.HTTP_200_OK
    )
@api_view(['POST'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_enrolled_courses(request):
        course = Course.objects.filter(students=request.user)
        serializer = CourseSerializer(course, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CourseViewSet(ModelViewSet):

    queryset = Course.objects.all()

    serializer_class = CourseSerializer

    permission_classes = [
        IsAuthenticated,
        IsInstructorOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    @action(detail=True,methods=['post'],permission_classes=[IsAuthenticated,IsInstructorOrReadOnly])
    def enroll(self, request, pk=None):
     course = self.get_object()

     if course.students.filter(id=request.user.id).exists():
        return Response(
            {"message": "You are already enrolled in this course."},
            status=status.HTTP_400_BAD_REQUEST
        )

     course.students.add(request.user)

     return Response(
        {"message": "Successfully enrolled."},
        status=status.HTTP_200_OK
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unenroll(self,request,pk=None):
         course = self.get_object()
         if not course.students.filter(id=request.user.id).exists():
             return Response(
                 {"message": "You are not enrolled in this course."},status=status.HTTP_400_BAD_REQUEST)
         
         course.students.remove(request.user)
         return Response(
             {"message": "Successfully unenrolled."},
             status=status.HTTP_200_OK
         )
  
   