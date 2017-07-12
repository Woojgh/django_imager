from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from user_images.models import Photo, Album, Item, AddImage
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from user_images.models import ImageUploadForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from imager_profile.forms import DocumentForm


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
    albums = Album.objects.all()
    context = {
        "photos": photos,
        "albums": albums,
        }
    # import pdb; pdb.set_trace()
    return render(request, 'user_images/user_images.html', context=context)


def add_image_view(request):
    # context = {'image': image}
    # return render(request, 'user_images/add_image.html', context=context)
    form = ImageUploadForm()
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            import pdb; pdb.set_trace()
            images = AddImage.objects.all()
            # m = ExampleModel.objects.get(pk=course_id)
            images.image = form.cleaned_data['image']
            for image in images:
                image.save()
            return HttpResponseRedirect("../user_images/add_image.html", {"form": form})

    return render(request, "user_images/add_image.html", {"form": form})




def thumb_view(request):
    items = Item.objects.all()
    context = {
        "items": items,
        }
    return render(request, 'user_images/thumb.html', context=context)
