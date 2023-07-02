from django.db import models
from simpleBooks_backend.users.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=13)
    publication_date = models.DateField()
    total_pages = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    resume = models.TextField()
    genre = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='book_covers/')
    # author = models.ForeignKey('Author', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reading_status_porcentaje = models.IntegerField()
    finished = models.BooleanField(default=False)