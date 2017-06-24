"""Model for our user images."""
from django.db import models
from django.contrib.auth.models import User


PUBLISHED_CHOICES = [
    ("public", "Public"),
    ("private", "Private"),
    ("shared", "Shared")
]


class Photo(models.Model):
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to='images/%Y-%m-%d')
    title = models.CharField(max_length=140, blank=False)
    description = models.CharField(max_length=200, blank=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)
    published = models.CharField(choices=PUBLISHED_CHOICES, default='public', max_length=10)

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

    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.user.id, filename)


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
        image: {}
        title: {}
        description: {}
        date_uploaded: {}
        date_modified: {}
        date_published: {}
        published: {}
        """.format(self.user, self.image, self.title, self.description, self.date_uploaded, self.date_modified, self.date_published, self.published)
