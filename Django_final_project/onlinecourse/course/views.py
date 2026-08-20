from django.http import HttpResponse
from .forms import ReviewForm
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Course,Category,Review,lesson,LessonCompletion
from django.core.paginator import Paginator
# Create your views here.

def course_list(request):
    # Logic to retrieve courses from the database
    courses = Course.objects.all()
    paginator = Paginator(courses, 5)  # Show 5 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'courses/courses2_list.html', {'page_obj': page_obj})
def coursedetail(request,id):
    if request.method == 'POST':
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.course=Course.objects.get(id=id)
            review.user=request.user
            review.save()
            return redirect('coursedetail', id=id)
    else:
        form=ReviewForm()
    course = Course.objects.get(id=id)
    lessons = lesson.objects.filter(course=course)
    count=0;
    return render(request,'courses/course_detail.html',{'course':course, 'form': form,'lessons':lessons,'count':count})
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
        return render(request, 'courses/search_list.html', {'courses': courses})
       else:
        categories = Category.objects.all()
        return render(request, 'courses/courses_list.html', {'categories': categories})
def category_detail(request, id):
        
    category = Category.objects.get(id=id)
    courses = Course.objects.filter(category=category)
    return render(request, 'courses/category_detail.html', {'category': category, 'courses': courses})
def lesson_detail(request, id):
    lesson_obj = lesson.objects.get(id=id)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson_obj})
@login_required
def mark_lesson_completed(request, id):

    lesson=lesson.objects.get(id=id)
    LessonCompletion.objects.create(lesson=lesson, user=request.user)
    return redirect('lesson_detail', id=id)