# Generated by Django 3.2 on 2023-07-19 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_lecture_goal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlecturegoal',
            name='goal_book_per_year',
        ),
        migrations.RemoveField(
            model_name='userlecturegoal',
            name='goal_sessions_per_day',
        ),
    ]
