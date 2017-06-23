"""django_imager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url, static
# from django.http import HttpResponse
# from django.template import loader
from django.contrib import admin
from imager_profile.views import home_view
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', home_view, name="home"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include('user_images')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'django_imager/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/accounts/profile'}, name='logout'),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.STATIC_ROOT
        )
