from django.db import models

from simpleBooks_backend.books.models import Book
from simpleBooks_backend.users.models import User


class ReadingSession(models.Model):
    time_of_reading = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)