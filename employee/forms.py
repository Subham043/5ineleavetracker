from django.forms import ModelForm, Textarea, DateInput, TextInput
from django import forms
from .models import Personal, work, BankAccount, Experience, Education
from django.utils import timezone

class DateInput(forms.DateInput):
    input_type = 'date'

class PersonalForm(ModelForm):
    class Meta:
        model = Personal
        fields = ['Mobile_Phone', 'Other_Email', 'Address', 'Date_Of_Birth', 'MARITAL_STATUS', 'Gender']
        MARITAL_STATUS_CHOICES = (
            ('SG', 'Single'),
            ('MD', 'Married'),
        )
        GENDER_CHOICES = (
            ('ML', 'Male'),
            ('FL', 'Female'),
        )
        widgets = {
            'Mobile_Phone': TextInput(attrs={'class' : 'form-control'}),
            'Other_Email': TextInput(attrs={'class' : 'form-control'}),
            'Address': Textarea(attrs={'class' : 'form-control'}),
            'Date_Of_Birth': DateInput(attrs={'class' : 'form-control'}),
            'MARITAL_STATUS': forms.Select(choices=MARITAL_STATUS_CHOICES,attrs={'class': 'form-control'}),
            'Gender': forms.Select(choices=GENDER_CHOICES,attrs={'class': 'form-control'}),
        }

class WorkForm(ModelForm):
    class Meta:
        model = work
        fields = ['Department','Reporting_To','Source_Of_Hire','Location','Title','Date_Of_Joining','Employee_Status','Employee_Type','Work_Phone','Extension','Role']
        widgets = {
            'Date_Of_Joining': DateInput(attrs={'class' : 'form-control'}),
        }

class BankAccountForm(ModelForm):
    class Meta:
        model = BankAccount
        fields = ['Bank_Name','Account_Number','Branch_Name','IFSC_Code']


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ['Previous_Company_Name','Job_Title','From','To','Job_Description']
        widgets = {
            'From': DateInput(attrs={'class' : 'form-control'}),
            'To': DateInput(attrs={'class' : 'form-control'}),
        }

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['School_Name','Degree_Or_Diploma','Field_Of_Study','Date_Of_Completion','Interests']
        widgets = {
            'Date_Of_Completion': DateInput(attrs={'class' : 'form-control'}),
        }