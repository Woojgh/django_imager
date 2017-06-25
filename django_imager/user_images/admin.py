from django.contrib import admin
from .models import Item
from sorl.thumbnail.admin import AdminImageMixin

from .models import Photo
from .models import Album


class PhotoAdmin(admin.ModelAdmin):
    """."""
    list_display = ('title', 'user', 'id')


class ItemAdmin(AdminImageMixin, admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album)
