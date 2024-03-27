from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_user_set', blank=True, help_text='The groups this user belongs to.')
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_user_set', blank=True, help_text='Specific permissions for this user.')


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.username}: {self.otp}"    