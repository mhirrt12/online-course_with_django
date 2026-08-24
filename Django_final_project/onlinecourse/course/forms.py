from django import forms
from .models import Review, Course,lesson

class ReviewForm(forms.ModelForm):

    rating = forms.ChoiceField(
        choices=[
            (1, '⭐'),
            (2, '⭐⭐'),
            (3, '⭐⭐⭐'),
            (4, '⭐⭐⭐⭐'),
            (5, '⭐⭐⭐⭐⭐'),
        ],
        widget=forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write your review...'
            }),
        }
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