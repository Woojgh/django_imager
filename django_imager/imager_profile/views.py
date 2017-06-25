from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from user_images.models import Photo
# from user_images.models import Album


def home_view(request):
    """Home view callable, for the home page."""
    context = {'food': 'steak'}
    return render(request, 'django_imager/home.html', context=context)


def account_view(request):
    return render(request, 'django_imager/account.html')


def profile_view(request):
    return render(request, 'django_imager/profile.html')


def logout_view(request):
    # message user or whatever
    return auth_views.logout(request)


def image_view(request):
    photos = Photo.objects.all()
    context = {"photos": photos}
    # import pdb; pdb.set_trace()
    return render(request, 'user_images/user_images.html', context=context)
