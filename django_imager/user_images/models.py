"""Model for our user images."""
from django.db import models
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User


PUBLISHED_CHOICES = [
    ("public", "Public"),
    ("private", "Private"),
    ("shared", "Shared")
]


class Photo(models.Model):
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to='uploaded_images/%Y-%m-%d', null=True)
    title = models.CharField(max_length=140, blank=False)
    description = models.CharField(max_length=200, blank=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)
    published = models.CharField(choices=PUBLISHED_CHOICES, default='public', max_length=10)

    def __repr__(self):
        """."""
        # return "<Photo: {}>".format(self.title)
        return """
        user: {}
        image: {}
        title: {}
        description: {}
        date_uploaded: {}
        date_modified: {}
        date_published: {}
        published: {}
        """.format(self.user, self.image, self.title, self.description, self.date_uploaded, self.date_modified, self.date_published, self.published)


class Item(models.Model):
    image = ImageField(upload_to='thumbnails', null=True)

    def __repr__(self):
        """."""
        return """
        image: {}
        """.format(self.image)


class Album(models.Model):
    user = models.ForeignKey(User)
    photo = models.ManyToManyField(Photo)
    title = models.CharField(max_length=140, blank=False)
    description = models.CharField(max_length=200, blank=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)
    published = models.CharField(choices=PUBLISHED_CHOICES, default='public', max_length=10 )

    def __repr__(self):
        """."""
        return """
        user: {}
        photo: {}
        title: {}
        description: {}
        date_uploaded: {}
        date_modified: {}
        date_published: {}
        published: {}
        """.format(self.user, self.photo, self.title, self.description, self.date_uploaded, self.date_modified, self.date_published, self.published)
