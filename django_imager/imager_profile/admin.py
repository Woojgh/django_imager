from django.contrib import admin
from imager_profile.models import ImagerProfile
admin.site.register(ImagerProfile)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'creation_date')
