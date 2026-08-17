from django.http import HttpResponse

from django.shortcuts import render

from .models import Course

# Create your views here.

def course_list(request):
    # Logic to retrieve courses from the database
    courses = Course.objects.all()
    return render(request, 'courses/courses_list.html', {'course': courses})
