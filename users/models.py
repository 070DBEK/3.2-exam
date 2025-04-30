from django.contrib.auth.models import AbstractUser
from django.db import models
from command.models import BaseModel


class User(AbstractUser, BaseModel):
    is_teacher = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)