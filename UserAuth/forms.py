from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )

class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']
