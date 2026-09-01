from django.urls import path
from . import views

urlpatterns=[path('courses/',views.course_list_api,name="course_list_api"),
             path('category/',views.category_list_api, name='categoty_list_api'),
             path('onecourse/',views.one_course, name='one_course'),
           path(
    'courses/<int:id>/',
    views.CourseDetailAPIView.as_view(),
    name='course_detail_api'
)]