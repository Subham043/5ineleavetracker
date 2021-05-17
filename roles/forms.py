from django.forms import ModelForm, Textarea, DateInput, TextInput
from django import forms
from .models import roles
from django.utils import timezone

class RoleForm(ModelForm):
    class Meta:
        model = roles
        fields = ['Role_Name',]