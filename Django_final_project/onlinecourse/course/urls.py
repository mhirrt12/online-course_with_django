from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path("<int:id>",views.coursedetail,name="coursedetail"),
    path("enroll/",views.enroll, name='enroll')
]