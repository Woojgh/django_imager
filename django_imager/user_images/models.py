from django.db import models
import datetime


class Images(models.Model):
    upload = models.ImageField(upload_to='users_images')
    date_added = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
