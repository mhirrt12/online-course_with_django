from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path("<int:id>",views.coursedetail,name="coursedetail"),
    path("enroll/<int:id>",views.enroll,name='enroll'),
    path("mycourse/",views.mycourse,name='mycourse'),
    path("unenroll/<int:id>",views.unenroll,name='unenroll'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path("page/",views.course_list,name='course_list'),
    path("lesson/<int:id>/", views.lesson_detail, name='lesson_detail'),
    path("lesson/<int:id>/complete/", views.mark_lesson_completed, name='mark_lesson_completed'),
    path("certificate/<int:id>/", views.certificate_detail, name='certificate_detail'),
    path("save_course/<int:id>/", views.save_course, name='save_course'),
    path("unsave_course/<int:id>/", views.unsave_course, name='unsave_course'),
    path("saved_courses/", views.saved_courses, name='saved_courses'),
    path(
    "notifications/",
    views.notifications,
    name="notifications"
),
    path(
    "instructor_dashboard/",
    views.instructor_dashboard,
    name="instructor_dashboard"),
    path(
    "create-course/",
    views.create_course,
    name="create_course"
),
path(
    "edit-course/<int:id>/",
    views.edit_course,
    name="edit_course"
),
path(
    "delete-course/<int:id>/",
    views.delete_course,
    name="delete_course"
),
path(
    "create-lesson/<int:course_id>/",
    views.create_lesson,
    name="create_lesson"
),path(
    "view-lesson/<int:course_id>/",
    views.view_course_lesson,
    name="view_course_lesson")
,path("edit-lesson/<int:lesson_id>/", views.edit_lesson, name="edit_lesson"),
path("delete-lesson/<int:lesson_id>/", views.delete_lesson, name="delete_lesson"),
path("edit-review/<int:review_id>/",views.edit_review ,name="edit_review"),
]