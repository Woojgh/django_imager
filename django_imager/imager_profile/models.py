from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# from django
PHOTO_CHOICES = [
    ("BW", "Black and White"),
    ("PAN", "Panorama"),
    ("PQR", "Panorama"),
    ("LAND", "Panorama"),
    ("COL", "Panorama"),
    ("PAN", "Panorama")
]


# class ImageActiveProfile(models.Manager)

class ImagerProfile(models.Model):
    """Users model when joining"""
    # user = OneToOne
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
    # date_joined = models.DateTimeField(('date joined'), default=timezone.now)

    username = models.CharField(
        ('username'),
        max_length=30,
        unique=True,
        help_text=('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')
        )
    location = models.CharField(max_length=20)
    # age = models.IntegerField(chioces=AGE_CHOICES)
    # camera_type = models.ChatField(choices=CAMERA_CHOICES, max_length=3)
    objects = models.Manager()
    # active = ImageActiveProfile()

    @property
    def is_active(self):
        return self.user.is_active

    def __repr__(self):
        return """
        first_name: {}
        last_name: {}
        email: {}
        is_staff: {}
        is_active: {}
        date_joined: {}
        username: {}
        location: {}
        age: {}
        camera: {}
        objects: {}
        active: {}
    """.format(self.user.username, self.photography_style, self.location, self.age, self.camera_type)


# @reciever(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    if kweargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance'],
            )
        new_profile.save()
