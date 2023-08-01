from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    lista_lenguajes = [
        ('es', 'Español'),
        ('en', 'English'),
    ]
    language = models.CharField(max_length=2, choices=lista_lenguajes, default='es')
    username = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True)
    token = models.CharField(max_length=100, unique=True, null=True, blank=True)

    email = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name']

    def generate_reset_token(self):
        # Generar el token utilizando la librería uuid
        reset_token = str(uuid.uuid4())
        self.token = reset_token
        self.save()
        return reset_token