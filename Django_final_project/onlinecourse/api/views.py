from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from course.models import Course
from .serializers import CourseSerializer

 @api_view(['GET'])