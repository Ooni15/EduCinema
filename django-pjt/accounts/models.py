from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    major = models.CharField(max_length=100)
    bio = models.TextField(blank=True)


