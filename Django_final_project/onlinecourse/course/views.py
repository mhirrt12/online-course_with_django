from django.http import HttpResponse

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course,Category

# Create your views here.

def course_list(request):
    # Logic to retrieve courses from the database
    courses = Course.objects.all()
    return render(request, 'courses/courses_list.html', {'courses': courses})
def coursedetail(request,id):
    course = Course.objects.get(id=id)
    return render(request,'courses/course_detail.html',{'course':course})
@login_required
def enroll(request,id):
    course=Course.objects.get(id=id)
    course.students.add(request.user)
    return HttpResponse("You have successfully enrolled in the course.")
@login_required
def mycourse(request):
    courses=request.user.course_set.all()
    return render(request,'courses/enrolled.html',{'mycourse':courses})
    # return HttpResponse("You have successfully enrolled in the course.")
def unenroll(request,id):
    course=Course.objects.get(id=id)
    course.students.remove(request.user)
    return HttpResponse("You have successfully unenrolled from the course.")
def category_list(request):
    query=request.GET.get('q')
    if query:
        courses=Course.objects.filter(title__icontains=query)
    else:
        courses = Course.objects.all()
    categories = Category.objects.all()
    return render(request, 'courses/courses_list.html', {'categories': categories, 'courses': courses})
def category_detail(request, id):
        
    category = Category.objects.get(id=id)
    courses = Course.objects.filter(category=category)
    return render(request, 'courses/category_detail.html', {'category': category, 'courses': courses})