from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    students =models.ManyToManyField(User)
    title = models.CharField(max_length=200)
    description = models.TextField()
    # enroll=models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
class Category(models.Model):
    
    name=models.CharField(max_length=100)
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name