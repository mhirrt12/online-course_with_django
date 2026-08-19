from django.contrib import admin

# Register your models here.

from .models import Course,Category

admin.site.register(Course,Category)