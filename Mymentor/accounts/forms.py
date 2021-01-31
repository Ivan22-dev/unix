from django.forms import ModelForm
from app1.models import *
from django import forms




class accforms(forms.ModelForm):
    class Meta(object):
        model = Account
        fields = ['username', 'email', 'password','status']
        