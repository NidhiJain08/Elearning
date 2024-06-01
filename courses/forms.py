from django import forms
from django.db.models import fields
from .models import Course,Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'thumbnail', 'category', 'short_description', 'description', 'language']
        
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title','video']