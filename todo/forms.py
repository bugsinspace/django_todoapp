from django.forms import ModelForm
from django import forms
from .models import Todo, Setting
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class SignUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_email = User.objects.filter(email=email).count()
        if user_email > 0:
            raise forms.ValidationError("This email has been already taken.")
        return email

class SettingForm(ModelForm):
    class Meta:
        model = Setting
        fields = ['avatar', 'bio']