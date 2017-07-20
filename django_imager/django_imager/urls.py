
from django.conf.urls import include, url
from django.contrib import admin
from imager_profile.views import album_view, home_view, add_image_view, profile_view, logout_view, library_view, thumb_view, add_album_view, edit_image, edit_album
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', home_view.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', profile_view.as_view(), name='profile'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', logout_view.as_view()),
    url(r'^library/$', library_view.as_view(), name='library'),
    url(r'^album/$', album_view.as_view()),
    url(r'^thumb/$', thumb_view, name='thumb'),
    url(r'^add_image/$', add_image_view.as_view(), name='add_image'),
    url(r'^add_album/$', add_album_view, name='add_album'),
    url(r'^edit_image/(?P<id>\d+)/$', edit_image.as_view(), name='edit_image'),
    url(r'^edit_album/$', edit_album.as_view()),
    url(r'^', include('imager_api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
        )
