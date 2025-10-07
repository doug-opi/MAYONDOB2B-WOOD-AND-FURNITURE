from django import forms
from django.contrib.auth.models import User
from .models import Profile

class AttendantCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['role']

    def save(self, created_by=None):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        profile = Profile.objects.create(user=user, role='attendant', created_by=created_by)
        return user
