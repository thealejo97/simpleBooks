# Generated by Django 3.2 on 2023-07-22 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_alter_book_publication_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='readed_pages',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]