from http.client import HTTPResponse

from django.shortcuts import render

from .models import Course

# Create your views here.

def course_list(request):
    # Logic to retrieve courses from the database
    courses = Course.objects.all()
    return render(request, 'courses/courses_list.html', {'courses': courses})
def home(request):
    return HTTPResponse("<h1>Welcome to the Online Course Platform</h1><p>Explore our courses and start learning today!</p>")