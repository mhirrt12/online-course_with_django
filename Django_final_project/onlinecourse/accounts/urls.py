from . import views
from django.urls import path
urlpattern=[path("",views.register,name="register")]