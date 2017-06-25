"""Model for our imager profiles."""
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
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
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    ('21', '21'),
    ('22', '22'),
    ('23', '23'),
    ('24', '24'),
    ('25', '25'),
    ('26', '26'),
    ('27', '27'),
    ('28', '28'),

]


class ImagerProfile(models.Model):
    """Users model when joining"""
    user = models.OneToOneField(
        User,
        default=True,
        related_name="+",
        null=False
    )
    date_joined = models.DateField(auto_now_add=True, null=True)
    location = models.CharField(max_length=20, blank=True)
    age = models.CharField(choices=AGE_CHOICES, default=18, max_length=150)
    camera_type = models.CharField(choices=CAMERA_CHOICES, max_length=150, default='Phillips')
    objects = models.Manager()

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
    """.format(self.user, self.age, self.first_name, self.last_name, self.email, self.is_staff, self.is_active, self.username, self.location, self.camera_type, self.objects)


@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance'],
        )
        new_profile.save()
