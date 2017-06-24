from django.shortcuts import render, render_to_response
from models import Images
# Create your views here.


def index(request):
    img = Images.objects.all()  # .order_by('-id')
    return render_to_response("images/user_images.html", {"img": img})