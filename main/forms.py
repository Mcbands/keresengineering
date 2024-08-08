from django import forms
from .models import Course

class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'level', 'duration', 'category', 'requirements', 'content', 'lesson_title',)

