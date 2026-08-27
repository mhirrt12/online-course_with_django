from django.http import HttpResponseForbidden,HttpResponse
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .forms import ReviewForm, CourseForm, LessonForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course,Category,Review,lesson,LessonCompletion,Certificate,Notification 
from django.core.paginator import Paginator
from django.db.models import Avg,Q
# Create your views here.
def instructor_required(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.profile.role != 'instructor':
            return HttpResponseForbidden("only instructor can access this page.")
        return view_func(request,*args,**kwargs)
    return wrapper
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
    # lesson=lesson.objects.filter(course=course)
    completed_lessons = LessonCompletion.objects.filter(user=request.user, lesson__course=course)
    total_lessons = lessons.count()
    completed_count = completed_lessons.count()
    if total_lessons > 0:
        progress_percentage = (completed_count / total_lessons) * 100
    else:
        progress_percentage = 0
    review_count = Review.objects.filter(
    course=course
).count()
    average_rating = Review.objects.filter(
    course=course
).aggregate(
    Avg('rating')
)['rating__avg']
    reviews=Review.objects.filter(course=course)
    return render(request,'courses/course_detail.html',{'course':course, 'form': form,'lessons':lessons, 'progress_percentage': progress_percentage,'average_rating': average_rating, 'review_count': review_count,'reviews':reviews})
@login_required
def enroll(request,id):
    course=Course.objects.get(id=id)
    course.students.add(request.user)
    Notification.objects.create(
    user=request.user,
    message=f"You enrolled in {course.title}!"
)
    return HttpResponse("You have successfully enrolled in the course.")
@login_required
def mycourse(request):
    courses = request.user.enrolled_courses.all()

    dashboard_courses = []

    for course in courses:

        lessons = lesson.objects.filter(
            course=course
        )

        completed_lessons = LessonCompletion.objects.filter(
            user=request.user,
            lesson__course=course
        )

        total_lessons = lessons.count()
        completed_count = completed_lessons.count()

        if total_lessons > 0:
            progress_percentage = (
                completed_count / total_lessons
            ) * 100
        else:
            progress_percentage = 0

        dashboard_courses.append({
            'course': course,
            'progress': progress_percentage
        })

    return render(
        request,
        'courses/enrolled.html',
        {
            'dashboard_courses': dashboard_courses
        }
    )
def unenroll(request,id):
    course=Course.objects.get(id=id)
    course.students.remove(request.user)
    return HttpResponse("You have successfully unenrolled from the course.")
def category_list(request):
       query=request.GET.get('q')
       if query:
        courses=Course.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))
        return render(request, 'courses/search_list.html', {'courses': courses})
       else:
        categories = Category.objects.all()
        return render(request, 'courses/courses_list.html', {'categories': categories})
def category_detail(request, id):
        
    category = Category.objects.get(id=id)
    courses = Course.objects.filter(category=category)
    return render(request, 'courses/category_detail.html', {'category': category, 'courses': courses})
@login_required
def lesson_detail(request, id):
    lesson_obj = lesson.objects.get(id=id)

    if request.user not in lesson_obj.course.students.all():
        return HttpResponseForbidden(
            "You must enroll in this course first."
        )

    return render(
        request,
        'courses/lesson_detail.html',
        {'lesson': lesson_obj}
    )
@login_required
def mark_lesson_completed(request, id):

    # 1. Get the lesson
    lesson_obj = get_object_or_404(lesson, id=id)

    # 2. Get the course that this lesson belongs to
    course = lesson_obj.course

    # 3. Create completion only if it doesn't already exist
    LessonCompletion.objects.get_or_create(
        lesson=lesson_obj,
        user=request.user
    )

    # 4. Get all lessons in this course
    lessons = lesson.objects.filter(
        course=course
    )

    # 5. Get lessons completed by this user
    completed_lessons = LessonCompletion.objects.filter(
        user=request.user,
        lesson__course=course
    )

    # 6. Count them
    total_lessons = lessons.count()
    completed_count = completed_lessons.count()
    if total_lessons > 0 and completed_count == total_lessons:

     Certificate.objects.get_or_create(
        user=request.user,
        course=course
    )

    # 7. Calculate progress
    if total_lessons > 0:
        progress_percentage = (
            completed_count / total_lessons
        ) * 100
    else:
        progress_percentage = 0

    # 8. If all lessons are completed, create certificate
    if progress_percentage >= 100:

        Certificate.objects.get_or_create(
            course=course,
            user=request.user
        )

    # 9. Return to lesson
    return redirect('lesson_detail', id=id)
@login_required
def certificate_detail(request, id):
    certificate = Certificate.objects.get(id=id, user=request.user)
    return render(request, 'courses/certificate_detail.html', {'certificate': certificate})

@login_required
def save_course(request, id):
    course = Course.objects.get(id=id)

    course.saved_by.add(request.user)

    return redirect('coursedetail', id=id)
@login_required
def unsave_course(request, id):
    course = Course.objects.get(id=id)

    course.saved_by.remove(request.user)

    return redirect('coursedetail', id=id)
@login_required
def saved_courses(request):
    courses = request.user.saved_courses.all()
    return render(request, 'courses/saved_courses.html', {'courses': courses})
@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    return render(
        request,
        'courses/notifications.html',
        {'notifications': notifications}
    )
    
@login_required
@instructor_required
def instructor_dashboard(request):
    courses = request.user.created_courses.all()
    
    return render(
        request,
        'courses/instructor_dashboard.html',
        {'courses': courses}
    )
    
@login_required
@instructor_required
def create_course(request):

    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()

            return redirect('instructor_dashboard')

    else:
        form = CourseForm()

    return render(
        request,
        'courses/create_course.html',
        {'form': form}
    )
@login_required
@instructor_required
def edit_course(request, id):
    course = Course.objects.get(id=id, instructor=request.user)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)

        if form.is_valid():
            form.save()
            return redirect('instructor_dashboard')

    else:
        form = CourseForm(instance=course)

    return render(
        request,
        'courses/edit_course.html',
        {'form': form}
    )
@login_required
@instructor_required
def delete_course(request, id):
    course = Course.objects.get(
        id=id,
        instructor=request.user
    )

    course.delete()

    return redirect('instructor_dashboard')
@login_required
@instructor_required
def create_lesson(request, course_id):  
    course = Course.objects.get(id=course_id, instructor=request.user)

    if request.method == 'POST':
        form = LessonForm(request.POST)

        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()

            return redirect('instructor_dashboard')
    else:
        form = LessonForm()

    return render(
        request,
        'courses/create_lesson.html',
        {'form': form, 'course': course}
    )
@login_required
def view_course_lesson(request, course_id):
    course = Course.objects.get(id=course_id)
    lesson_obj = course.lesson_set.all()
    return render(request, 'courses/view_lesson.html', {'lesson': lesson_obj})
@login_required
@instructor_required
def manage_lessons(request, course_id):

    course = Course.objects.get(
        id=course_id,
        instructor=request.user
    )

    lessons = lesson.objects.filter(
        course=course
    )

    return render(
        request,
        'courses/manage_lessons.html',
        {
            'course': course,
            'lessons': lessons
        }
    )
@login_required
@instructor_required
def edit_lesson(request, lesson_id):
    lesson_obj = lesson.objects.get(
    id=lesson_id,
    course__instructor=request.user
)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson_obj)

        if form.is_valid():
            form.save()
            return redirect('view_course_lesson', course_id=lesson_obj.course.id)
    else:
        form = LessonForm(instance=lesson_obj)

    return render(
        request,
        'courses/edit_lesson.html',
        {'form': form, 'lesson': lesson_obj}
    )
@login_required
@instructor_required
def delete_lesson(request, lesson_id):
    lesson_obj = lesson.objects.get(id=lesson_id)
    course_id = lesson_obj.course.id
    lesson_obj.delete()
    return redirect('view_course_lesson', course_id=course_id)
@login_required  
def edit_review(request,review_id):
    review=Review.objects.get(id=review_id,user=request.user)
    if request.method=="POST":
        form=ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("coursedetail",id=review.course.id)
    else :
            form=ReviewForm(instance=review)
    return render(request,'courses/edit_review.html',{'form':form,'review':review})
  

@login_required
def delete_review(request,review_id):
    review=Review.objects.get(id=review_id,user=request.user)
    review.delete()
    return redirect("coursedetail",id=review.course.id)
@login_required
def my_learning(request):

    courses = request.user.enrolled_courses.all()

    course_progress = []

    for course in courses:

        total_lessons = lesson.objects.filter(
            course=course
        ).count()

        completed_lessons = LessonCompletion.objects.filter(
            user=request.user,
            lesson__course=course
        ).count()

        if total_lessons > 0:
            progress = (completed_lessons / total_lessons) * 100
        else:
            progress = 0
            
        remaining_lessons = total_lessons - completed_lessons
        certificate = None
        
        if completed_lessons == total_lessons and total_lessons > 0:
                   certificate = Certificate.objects.filter(
                             user=request.user,
                                 course=course
                                   ).first()
        course_progress.append({
            'course': course,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress': progress,
            'remaining_lessons':remaining_lessons,
                'completed': completed_lessons == total_lessons and total_lessons > 0,
               'certificate': certificate,
        })
       
    return render(
        request,
        'courses/my_learning.html',
        {'course_progress': course_progress}
    )
@login_required
def certificate_view(request, course_id):

    certificate = Certificate.objects.get(
       id=course_id, user=request.user
        
    )
  

    return render(
        request,
        'courses/certificate.html',
        {'certificate': certificate}
    )
@login_required
def download_certificate(request, id):

    certificate = Certificate.objects.get(
        id=id,
        user=request.user
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="certificate_{certificate.id}.pdf"'
    )

    pdf = canvas.Canvas(response, pagesize=A4)

    width, height = A4

    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        width / 2,
        height - 100,
        "CERTIFICATE OF COMPLETION"
    )

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 180,
        "This certifies that"
    )

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(
        width / 2,
        height - 230,
        certificate.user.get_full_name()
        or certificate.user.username
    )

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 280,
        "has successfully completed"
    )

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(
        width / 2,
        height - 330,
        certificate.course.title
    )

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        width / 2,
        height - 390,
        f"Issued on: {certificate.issued_at.strftime('%B %d, %Y')}"
    )

    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        width / 2,
        height - 440,
        f"Certificate ID: {certificate.id}"
    )

    pdf.showPage()
    pdf.save()

    return response