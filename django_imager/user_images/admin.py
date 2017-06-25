from django.contrib import admin

from .models import Photo
from .models import Album


class PhotoAdmin(admin.ModelAdmin):
    """."""
    list_display = ('title', 'user', 'id')

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album)
