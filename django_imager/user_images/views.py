from django.shortcuts import render, render_to_response
from user_images.models import Photo
# Create your views here.


def index(request):
    img = Photo.objects.all()  # .order_by('-id')
    return render_to_response("images/user_images.html", {"img": img})