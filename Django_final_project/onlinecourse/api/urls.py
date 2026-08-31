from django.urls import path
from . import views

urlpatterns=[path('courses/',views.course_list_api,name="course_list_api")]