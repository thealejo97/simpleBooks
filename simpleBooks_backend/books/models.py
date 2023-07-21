from django.db import models
from simpleBooks_backend.users.models import User
from simpleBooks_backend.authors.models import Author


class Book(models.Model):
    lista_lenguajes = [
        ('es', 'Español'),
        ('en', 'English'),
    ]

    title = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=13, null=True,blank=True)
    publication_date = models.DateField(null=True,blank=True)
    publication_year = models.IntegerField(null=True,blank=True)
    total_pages = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    resume = models.TextField(null=True,blank=True)
    genre = models.CharField(max_length=255, null=True,blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True,blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reading_status_porcentaje = models.IntegerField(null=True,blank=True)
    finished = models.BooleanField(default=False, null=True,blank=True)
    language = models.CharField(max_length=2, choices=lista_lenguajes, default='es', null=True,blank=True)