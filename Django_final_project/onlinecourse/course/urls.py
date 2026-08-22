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
]