from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField()
    photo = models.ImageField(upload_to='authors/',null=True,blank=True)