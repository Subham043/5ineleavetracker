from django.forms import ModelForm, Textarea, DateInput, TextInput
from django import forms
from .models import department
from django.utils import timezone

class DepartmentForm(ModelForm):
    class Meta:
        model = department
        fields = ['Department_Name','Mail_Alias','Department_Lead']