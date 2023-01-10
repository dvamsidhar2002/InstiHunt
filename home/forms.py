from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SurveyForm():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        course = forms.CharField()
        course_duration = forms.CharField()
        program_type= forms.CharField()
        college_type= forms.CharField()
        avg_fee = forms.CharField()
        exam_accepted = forms.CharField()
        state= forms.CharField()
        city= forms.CharField()

    class Meta:
        fields=['course','course_duration','program_type','college_type','avg_fee','exam_accepted','state','city']
