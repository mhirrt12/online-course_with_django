from django.shortcuts import render

from Django_final_project.onlinecourse.course.models import Course

# Create your views here.

def course_list(request):
    # Logic to retrieve courses from the database
    courses = Course.objects.all()
    return render(request, 'course/course_list.html', {'courses': courses})