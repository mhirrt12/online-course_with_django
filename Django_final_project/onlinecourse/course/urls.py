from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path('courses/', views.course_list, name='course_list'),
]