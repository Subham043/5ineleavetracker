from django.forms import ModelForm, Textarea, DateInput, TextInput
from django import forms
from .models import designation
from django.utils import timezone

class DesignationForm(ModelForm):
    class Meta:
        model = designation
        fields = ['Designation_Name','Stream','Mail_Alias']