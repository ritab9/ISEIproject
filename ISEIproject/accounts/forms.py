from django.forms import ModelForm, modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms.models import inlineformset_factory
# from django.contrib.auth.models import User


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
        fields = ('school_year', 'date_submitted', 'summary')
        #widgets = {
        #    'school_year': forms.TextInput(attrs={'class': 'form-controls', 'placehoder': 'Enter school year'}),
        #    'date_submitted': forms.DateField(attrs={'class': 'form-controls', 'placehoder': 'Enter date'}),
        #    'summary': forms.Textarea(
        #        attrs={'class': 'form-controls', 'placehoder': 'Enter summary for combined activities'})
        #}


PDAInstanceModelFormset = modelformset_factory(
    PDAInstance,
    fields=('pda_type', 'date_completed', 'description', 'pages', 'clock_hours', 'ceu'),
    widgets={}
)


class PDAInstanceForm(forms.ModelForm):
    class Meta:
        model = PDAInstance
        fields = ('pda_type', 'date_completed', 'description', 'pages', 'clock_hours', 'ceu')



PDAInstanceFormSet = inlineformset_factory(PDARecord, PDAInstance, form=PDAInstanceForm, extra=1,
                                           can_delete=False)

class DocumentForm(forms.Form):
    name = forms.CharField(max_length=35, min_length=1)
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


#class SupportingDocumentForm(forms.ModelForm):
#    class Meta:
#       model = SupportingDocument
#       fields = ('document', )

#SupportingDocumentFormSet = inlineformset_factory(PDARecord, SupportingDocument, form=SupportingDocumentForm,can_delete=False, extra=1)