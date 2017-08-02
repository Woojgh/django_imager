from django.shortcuts import render
from django.contrib.auth import views as auth_views
from user_images.models import Photo, Album
from django.http import HttpResponseRedirect
from imager_profile.forms import ImageUploadForm, AlbumUploadForm, EditImageForm, EditAlbumForm
from django.core.urlresolvers import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from taggit.models import Tag


class home_view(View):
    """Home view callable, for the home page."""
    def get(self, request):
        return render(request, 'django_imager/home.html')


class profile_view(View):
    """Profile view callable, for the profile page"""
    def get(self, request):
        return render(request, 'django_imager/profile.html')


class logout_view(View):
    """Logout view callable, for the logout page"""
    def get(self, request):
        return auth_views.logout(request)


class album_view(View):
    """Album view callable, for the album page"""
    def get(self, request):
        album = Album.objects.all()
        context = {
            "album": album
            }
        return render(request, 'user_images/album_view.html', context=context)


class edit_album(View):
    """View for editing the abums that have been created."""
    form_class = EditAlbumForm
    initial = {'form': 'form'}
    template_name = 'user_images/edit_album.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save_m2m()
            # <process form cleaned data>
            return HttpResponseRedirect('/library/')

        return render(request, self.template_name, {'form': form})


class library_view(ListView):
    """View for the library or the page that shows all the users images and albums."""
    def get(self, request, page_num=1):
        albums = Album.objects.all()
        photos = Photo.objects.all()
        paginator = Paginator(photos, 3)
        page = request.GET.get('page')
        tags = Tag.objects.all()
        try:
            library_pages = paginator.page(page)
        except PageNotAnInteger:
            library_pages = paginator.page(1)
        except EmptyPage:
            library_pages = paginator.page(paginator.num_pages)

        context = {
            "photos": photos,
            "albums": albums,
            "library_pages": library_pages,
            "tags": tags
            }
        return render(request, 'user_images/user_images.html', context=context)


class edit_image(UpdateView):
    """View for editing images that have been uploadded to server."""
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
        photo = Photo.objects.get(pk=kwargs['pk'])
        request.POST = dict(request.POST)
        request.POST['user'] = request.user.id
        form = EditImageForm(request.POST, instance=photo)
        if form.is_valid():
            form.save(commit=False)
            form.save_m2m()
            return HttpResponseRedirect(reverse_lazy('library'))

        return render(request, self.template_name, {'form': form})


class add_image_view(View):
    """This is the view that is used when adding an image to the database."""
    form_class = ImageUploadForm
    initial = {'form': 'form'}
    template_name = 'user_images/add_image.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ImageUploadForm()
        photo = Photo()
        photo.title = request.POST['title']
        photo.description = request.POST['description']
        photo.published = request.POST['published']
        photo.user = request.user
        photo.image = request.FILES['image']
        photo.save()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('library'), {"form": form})

        return render(request, self.template_name, {'form': form})


class add_album_view(View):
    """View used for adding an album to the user."""
    form_class = ImageUploadForm
    initial = {'form': 'form'}
    template_name = 'user_images/add_image.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AlbumUploadForm()
        album = Album()
        album.title = request.POST['title']
        album.description = request.POST['description']
        album.published = request.POST['published']
        album.user = request.user
        album.image = request.FILES['image']
        album.save()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('library'), {"form": form})

        return render(request, self.template_name, {'form': form})


class thumb_view(View):
    """View used for looking at images thumbnails."""
    def get(self, request):
        items = Album.objects.all()
        context = {
            "items": items
            }
        return render(request, 'user_images/thumb.html', context=context)


class TagListView(ListView):
    """The listing for tagged books."""

    template_name = "user_images/library.html"

    def get_queryset(self):
        """Filter queryset by slug."""
        # import pdb; pdb.set_trace()
        return (Photo.objects.filter(tags__slug=self.kwargs.get("slug"))
                             .filter(published='PB')
                             .all())

    def get_context_data(self, **kwargs):
        """Return the context with the given tags."""
        context = super(TagListView, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("slug")
        return context
