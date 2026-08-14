from . import views
from django.urls import path
urlpattern=[
    path("register/",views.register,name="register")
    ]