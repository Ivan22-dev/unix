from django.forms import ModelForm
from app1.models import *
from django import forms



class itemforms(forms.ModelForm):
    class Meta(object):
        model = Items
        fields = ['name', 'code', 'program','points','sem_redovni','sem_izvanredni','izborni']

'''class enrforms(forms.ModelForm):
    class Meta(object):
        model = Enrollment
        fields = ['user_id', 'itemid', 'status']
'''


