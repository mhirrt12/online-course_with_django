from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
urlpatterns=[
    path("register/",views.register,name="register"),
    path("login/",views.login_view,name="login"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path('logout/', views.logout_view, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    ]