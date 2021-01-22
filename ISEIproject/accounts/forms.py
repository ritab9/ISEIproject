from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# from django.forms.models import inlineformset_factory
# from django.forms.models import BaseInlineFormSet
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'size': 1}),
        }


class PDARecordForm(ModelForm):
    class Meta:
        model = PDARecord
        fields = '__all__'
