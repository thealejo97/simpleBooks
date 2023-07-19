
from django.db import models

from simpleBooks_backend.books.models import Book
from ..users.models import User


class UserLectureGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_page_per_day = models.IntegerField()
    goal_reading_speed = models.IntegerField()
    goal_sessions_per_day = models.TimeField()
    goal_hours_per_day = models.TimeField()
    goal_book_per_year = models.TimeField()
    creation_date = models.DateTimeField(auto_now_add=True, null= True, blank=True)