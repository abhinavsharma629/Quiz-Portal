from django import forms
from .models import QuestionData
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
import csv
import os
from io import StringIO
import io

class RegistrationForm(UserCreationForm):
	class Meta:
		model= User
		fields=['username','first_name','password1','password2']


class LoginForm(AuthenticationForm):
	id_no=forms.CharField(widget=forms.TextInput(),required=True,max_length=100)
	password=forms.CharField(widget=forms.PasswordInput(),required=True,max_length=100)


class DataInput(forms.Form):
    file = forms.FileField()

    #CSV File Save to DataBase
    def save(self):
        file=self.cleaned_data["file"]
        decoded_file = file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        for line in csv.reader(io_string, delimiter=','):
            p=QuestionData(id_no=line[0], question=line[1], optionA=line[2],optionB=line[3], optionC=line[4], optionD=line[5], correct_choice=line[6])
            p.save()