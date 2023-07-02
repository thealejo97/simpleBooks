# Generated by Django 3.2 on 2023-07-02 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('es', 'Español'), ('en', 'English')], default='es', max_length=2),
        ),
    ]