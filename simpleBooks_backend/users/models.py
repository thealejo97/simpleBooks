from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    lista_lenguajes = [
        ('es', 'Español'),
        ('en', 'English'),
    ]
    language = models.CharField(max_length=2, choices=lista_lenguajes, default='es')
    username = models.EmailField(unique=True)
    email = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name']