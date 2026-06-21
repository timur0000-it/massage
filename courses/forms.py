from django import forms
from .models import *
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['teacher','students','max_slides','curent_slides','ready','extra_teachers']
class TextForm(forms.ModelForm):
    class Meta:
        model = Text_course
        exclude = ['course','slide']
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video_course
        exclude = ['course','slide']

class PracticeForm(forms.ModelForm):
    class Meta:
        model = Practice_course
        exclude = ['course','slide']

class Practice_StudentForm(forms.ModelForm):
    class Meta:
        model = Practice_answers
        exclude = ['student','practice','results','commentary','course']

