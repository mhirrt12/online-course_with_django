"""
URL configuration for onlinecourse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

# from ..course import views
def home(request):
    return HttpResponse("<h1>Welcome to the Online Course Platform</h1><p>Explore our courses and start learning today!</p>")
urlpatterns = [
    path('',home,name='home'),
    path('admin/', admin.site.urls),
    path('courses/', include('course.urls')),
    path("accounts/", include("accounts.urls")),
    # Include the course app's URLs
]
