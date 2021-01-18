from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

#from django.forms.models import inlineformset_factory
#from django.forms.models import BaseInlineFormSet
from .models import *

class CreateUserForm(UserCreationForm):
 	class Meta:
 		model = User
 		fields = ['username','first_name', 'last_name','email','password1','password2']


class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ('first_name','last_name','email')

class TeacherForm(ModelForm):
	class Meta:
		model = Teacher
		fields = '__all__'
		exclude = ['user']

class ActivityForm(ModelForm):
	#readonly_field = ['teacher']
	def __init__(self, *args, **kwargs):
		super(ActivityForm, self).__init__(*args, **kwargs)
		self.fields['teacher'].widget.attrs['readonly'] = True
		
	class Meta:
		model = Activity
		fields = '__all__'
	#disable teacher field in update	
		#	instance = getattr(self, 'instance', None)
	#	if instance and instance.pk:
	#		for field in self.readonly_field:
	
