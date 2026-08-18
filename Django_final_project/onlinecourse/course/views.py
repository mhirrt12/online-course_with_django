from django.http import HttpResponse

from django.shortcuts import render

from .models import Course

# Create your views here.

def course_list(request):
    # Logic to retrieve courses from the database
    courses = Course.objects.all()
    return render(request, 'courses/courses_list.html', {'courses': courses})
def coursedetail(request,id):
    course = Course.objects.get(id=id)
    return render(request,'courses/course_detail.html',{'course':course})
def enroll(request,id):
    course=Course.objects.get(id=id)
    course.students.add(request.user)
    return HttpResponse("You have successfully enrolled in the course.")
def mycourse(request):
    courses=request.user.course_set.all()
    return render(request,'courses/enrolled.html',{'mycourse':courses})
    # return HttpResponse("You have successfully enrolled in the course.")