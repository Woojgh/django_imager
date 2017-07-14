from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from user_images.models import Photo, Album
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from imager_profile.forms import ImageUploadForm, AlbumUploadForm, EditImageForm, EditAlbumForm
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from imager_profile.forms import DocumentForm
from django.views import View
from django.views.generic.edit import UpdateView


class home_view(View):
    """Home view callable, for the home page."""
    def get(self, request):
        return render(request, 'django_imager/home.html')


# def account_view(request):
#     return render(request, 'django_imager/account.html')


class profile_view(View):
    def get(self, request):
        return render(request, 'django_imager/profile.html')


class logout_view(View):
    def get(self, request):
        # message user or whatever
        return auth_views.logout(request)


class album_view(View):
    def get(self, request):
        album = Album.objects.all()
        context = {
            "album": album
            }
        return render(request, 'user_images/album_view.html', context=context)


class edit_album(View):
    form_class = EditAlbumForm
    initial = {'form': 'form'}
    template_name = 'user_images/edit_album.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/library/')

        return render(request, self.template_name, {'form': form})


class library_view(View):
    def get(self, request):
        photos = Photo.objects.all()
        albums = Album.objects.all()
        context = {
            "photos": photos,
            "albums": albums,
            }
        return render(request, 'user_images/user_images.html', context=context)


class edit_image(View):
    # import pdb; pdb.set_trace()
    model = Photo
    fields = ['title', 'description']
    template_name_suffix = '_update_form'
    form_class = EditImageForm
    initial = {'form': 'form'}
    template_name = 'user_images/edit_image.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = request.user
        data = request.POST
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url)

        return render(request, self.template_name, {'form': form})


def add_image_view(request):
    form = ImageUploadForm()
    if request.method == 'POST':
        photo = Photo()
        photo.title = request.POST['title']
        photo.description = request.POST['description']
        photo.published = request.POST['published']
        photo.user = request.user
        photo.image = request.FILES['image']
        photo.save()
        return HttpResponseRedirect(reverse_lazy('library'), {"form": form})

    return render(request, "user_images/add_image.html/", {"form": form})


def add_album_view(request):
    """View for adding an album to our image app."""
    form = AlbumUploadForm()
    if request.method == 'POST':
        album = Album()
        album.title = request.POST['title']
        album.description = request.POST['description']
        album.published = request.POST['published']
        album.user = request.user
        album.image = request.FILES['image']
        album.save()
        return HttpResponseRedirect(reverse_lazy('library'), {"form": form})

    return render(request, "user_images/add_album.html", {"form": form})


def thumb_view(request):
    items = Photo.objects.all()
    context = {
        "items": items,
        }
    return render(request, 'user_images/thumb.html', context=context)
