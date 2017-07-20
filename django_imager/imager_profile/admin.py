from django.contrib import admin
from imager_profile.models import ImagerProfile


class ImageAdmin(admin.ModelAdmin):
    list_display = ('username', 'user', ['tag_list'])

    def get_queryset(self, request):
        return super(MyModelAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

admin.site.register(ImagerProfile)
