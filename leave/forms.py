from django.forms import ModelForm, Textarea, DateInput, TextInput
from django import forms
from .models import LeaveType, ApplyLeave, HolidayList
from django.utils import timezone
from datetime import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class LeaveTypeForm(ModelForm):
    class Meta:
        model = LeaveType
        fields = ['Name','Code','Leave_Type','Unit','Description','Valid_From','Valid_To','Opening_Balance','Maximum_Balance', 'Holiday_Between_Leave_Period', 'To_Be_Applied_Days_In_Advance', 'Maximum_Number_Of_Consecutive_Days_Of_Leave_Allowed', 'Minimum_Gap_Between_2_Application_In_Days']
        widgets = {
            'Valid_From': DateInput(attrs={'class' : 'form-control'}),
            'Valid_To': DateInput(attrs={'class' : 'form-control'}),
        }

class ApplyLeaveForm(ModelForm):
    class Meta:
        model = ApplyLeave
        fields = ['Leave_Type','Valid_From','Valid_To','Team_Email_ID','Reason_For_Leave']
        widgets = {
            'Valid_From': DateInput(attrs={'class' : 'form-control', 'min':datetime.today().strftime('%Y-%m-%d')}),
            'Valid_To': DateInput(attrs={'class' : 'form-control', 'min':datetime.today().strftime('%Y-%m-%d')}),
        }

class HolidayListForm(ModelForm):
    class Meta:
        model = HolidayList
        fields = ['Name','Date','Description','Type','EveryYear']
        widgets = {
            'Date': DateInput(attrs={'class' : 'form-control'}),
        }