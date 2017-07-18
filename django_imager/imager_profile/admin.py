from django.contrib import admin
from imager_profile.models import ImagerProfile


class ImageAdmin(admin.ModelAdmin):
    list_display = ('username', 'user')

admin.site.register(ImagerProfile)
