from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class ProfileUpdateForm(forms.ModelForm):
    """Allow the user to update their profile image"""
    class Meta:
        model = UserProfile
        fields = ['image']
