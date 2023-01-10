from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = forms.CharField()
        email = forms.CharField()
        password1= forms.CharField()
        password2= forms.CharField()

    class Meta:
        model=User
        fields=['username','email','password1','password2']

class loginForm(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = forms.CharField()
        password= forms.CharField()
