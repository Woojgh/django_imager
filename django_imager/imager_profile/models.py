from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from datetime import datetime
from django.dispatch import receiver

PHOTO_CHOICES = [
    ("BW", "Black and White"),
    ("PAN", "Panorama"),
    ("PQR", "Panorama"),
    ("LAND", "Panorama"),
    ("COL", "Panorama"),
    ("PAN", "Panorama")
]

CAMERA_CHOICES = [
    ('Phillips', 'zoomandsuch'),
    ('yourface', 'nozoomforyou')
]

AGE_CHOICES = [
    ('15', '18'),
    ('19', '25'),
    ('26', '+')
]


class ImagerProfile(models.Model):
    """Users model when joining"""
    user = models.OneToOneField(
        User,
        default=True,
        related_name="+",
        null=False
    )
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    email = models.EmailField(('email address'), blank=True)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    # date_joined = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(choices=AGE_CHOICES, null=True)
    camera_type = models.CharField(choices=CAMERA_CHOICES, max_length=150, default='Phillips')
    objects = models.Manager()
    user_images = models.ImageField(default="nothing.jpg")

    @property
    def is_active(self):
        """."""
        return self.user.is_active

    def __repr__(self):
        """."""
        return """
        user: {}
        age: {}
        first_name: {}
        last_name: {}
        email: {}
        is_staff: {}
        is_active: {}
        date_joined: {}
        username: {}
        location: {}
        camera_type: {}
        objects: {}
        user_images: {}
    """.format(self.user, self.age, self.first_name, self.last_name, self.email, self.is_staff, self.is_active, self.username, self.location, self.camera_type, self.objects, self.user_images)

@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance'],
        )
        new_profile.save()
