
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from .models import TeacherProfile
from django.contrib.auth import get_user_model

class UserRegisterForm(forms.ModelForm):


    class Meta:
        model = CustomUser
        fields = ['email']






class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email']


class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['image','name','city', 'club', 'url_youtube', 'description']