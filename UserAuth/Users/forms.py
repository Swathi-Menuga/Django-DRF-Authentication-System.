from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class OTPVerificationForm(forms.Form):
    email_or_username = forms.CharField(label='Email or Username')
    otp = forms.CharField(label='OTP')

    def clean(self):
        cleaned_data = super().clean()
        email_or_username = cleaned_data.get("email_or_username")
        otp = cleaned_data.get("otp")