from . import views
from django.urls import path
urlpatterns=[
    path("register/",views.register,name="register"),
    path("login/",views.login,name="login"),
    path("dashboard/",views.dashboard,name="dashboard")
    ]