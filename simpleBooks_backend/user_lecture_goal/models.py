
from django.db import models

from simpleBooks_backend.books.models import Book
from ..users.models import User


class UserLectureGoal(models.Model):
    """
    Campos:
        velocidad_lectura OK
        page_per_day_avg_last_week OK
        sessions_per_day_sum_last_week OK
        readed_hours_day_last_week OK
        books_per_year OK
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_velocidad_lectura = models.IntegerField(null= True, blank=True)
    goal_page_per_day_last_week = models.IntegerField(null= True, blank=True)
    goal_sessions_per_day_sum_last_week = models.IntegerField(null= True, blank=True)
    goal_readed_hours_day_last_week = models.TimeField(null= True, blank=True)
    goal_book_per_year = models.IntegerField(null= True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, null= True, blank=True)