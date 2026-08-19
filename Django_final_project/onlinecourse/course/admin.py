from django.contrib import admin

# Register your models here.

from .models import Course,Catagory

admin.site.register(Course,Catagory)