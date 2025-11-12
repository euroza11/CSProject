from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Player

class RegisterForm(UserCreationForm):
    tel = forms.CharField(max_length=10, required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]

    def save(self, commit=True):
        user = super().save(commit=commit)
        tel = self.cleaned_data["tel"]
        Player.objects.create(user=user, tel=tel)
        return user
