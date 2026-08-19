from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
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
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.course.title} by {self.user.username}"