from django.db import models
from sorl.thumbnail import ImageField


class Images(models.Model):
    image = ImageField(upload_to='user_images/images', null=True)