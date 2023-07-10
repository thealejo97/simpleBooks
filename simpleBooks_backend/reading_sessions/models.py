from django.db import models

from simpleBooks_backend.books.models import Book
from simpleBooks_backend.users.models import User


class ReadingSession(models.Model):
    time_of_reading = models.TimeField()
    creation_date = models.TimeField(auto_now_add=True)
    readed_pages = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
