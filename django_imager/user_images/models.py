from django.db import models
import datetime


class Images(models.Model):
    image_upload = models.ImageField(upload_to='images', default='no.jpg')
    date_added = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
