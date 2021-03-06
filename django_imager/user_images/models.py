"""Model for our user images."""
from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager


PUBLISHED_CHOICES = [
    ("public", "Public"),
    ("private", "Private"),
    ("shared", "Shared")
]


class Photo(models.Model):
    """The model for when needing to add or manipulate images."""
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to='uploaded_images/%Y-%m-%d', null=True)
    title = models.CharField(max_length=140, blank=False)
    description = models.CharField(max_length=255, blank=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)
    published = models.CharField(choices=PUBLISHED_CHOICES, default='public', max_length=10)
    tags = TaggableManager()

    def __repr__(self):
        """."""
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


class Album(models.Model):
    """Model used for when dealing with albums."""
    user = models.ForeignKey(User)
    uploaded_images = models.ManyToManyField(Photo)
    image = models.ImageField(Photo, null=True)
    title = models.CharField(max_length=140, blank=False)
    description = models.CharField(max_length=255, blank=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)
    published = models.CharField(choices=PUBLISHED_CHOICES, default='public', max_length=10)
    tags = TaggableManager()

    def __repr__(self):
        """."""
        return """
        user: {}
        uploaded_images:{}
        image: {}
        title: {}
        description: {}
        date_uploaded: {}
        date_modified: {}
        date_published: {}
        published: {}
        """.format(self.user, self.uploaded_images, self.image, self.title, self.description, self.date_uploaded, self.date_modified, self.date_published, self.published)
