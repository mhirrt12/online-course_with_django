from django.contrib import admin

# Register your models here.

from .models import Course,Category,Review, lesson,Profile

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(lesson)
admin.site.register(Profile)