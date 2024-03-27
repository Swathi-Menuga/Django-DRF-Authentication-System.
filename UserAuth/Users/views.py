from django.shortcuts import render,redirect

# Create your views here.
# Users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as AuthUser
from django.shortcuts import get_object_or_404
from .models import OTP
from .forms import UserRegistrationForm
from django.core.mail import send_mail
import random
from .forms import OTPVerificationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate


def generate_otp():
    return str(random.randint(100000, 999999))

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Generate OTP
            otp = generate_otp()

            # Save OTP to the database
            OTP.objects.create(user=user, otp=otp)

            # Send OTP via email
            send_mail(
                'Your OTP for registration',
                f'Your OTP is: {otp}',
                'your_email@example.com',  # Update with your email address
                [user.email],  # Recipient's email address
                fail_silently=False,
            )

            return redirect('verify_otp')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data['email_or_username']
            otp_code = form.cleaned_data['otp']

            # Retrieve the user object based on the provided email/username
            user = get_object_or_404(AuthUser, email=email_or_username)  # Assuming email is used for verification

            # Retrieve the OTP object for the user
            otp = OTP.objects.filter(user=user, otp=otp_code).order_by('-created_at').first()

            if otp:
                otp.delete()
                return redirect('login_with_otp')
            else:
                return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    # If the request method is not POST or the form is invalid, render the OTP verification form
    else:
        form = OTPVerificationForm()

    return render(request, 'verify_otp.html', {'form': form})

def login_with_otp(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username')
        otp_code = request.POST.get('otp')

        user = authenticate(request, username=email_or_username, password=otp_code)

        if user is not None:
            OTP.objects.filter(user=user).delete()
            return redirect('profile')
        else:
            return render(request, 'login_with_otp.html', {'error': 'Invalid credentials'})
    return render(request, 'login_with_otp.html')



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login_with_otp')