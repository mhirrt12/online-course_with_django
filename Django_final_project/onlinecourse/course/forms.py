from django import forms
from .models import Review, Course,lesson

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'category',
        ]
class LessonForm(forms.ModelForm):
    class Meta:
        model = lesson
        fields = [
            'title',
            'content',
        ]