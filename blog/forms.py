# forms.py
from django import forms
from .models import UserComment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = ['comment_text']


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(
        max_length=254, help_text='Enter a valid email address')
    password = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
