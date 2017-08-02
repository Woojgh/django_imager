from django import forms
from user_images.models import Photo, Album


class DocumentForm(forms.Form):
    image = forms.FileField(
        label='Select a file',
    )


class ImageUploadForm(forms.ModelForm):
    """Image upload form."""
    class Meta:
        model = Photo
        exclude = ['user']


class EditImageForm(forms.ModelForm):

    class Meta:
        model = Photo
        exclude = ['user', 'date_uploaded', 'date_published', 'published', 'uploaded_images', 'image']


class AlbumUploadForm(forms.ModelForm):
    """Image upload form."""
    class Meta:
        model = Album
        exclude = ['user']


class EditAlbumForm(forms.ModelForm):
    """Album upload form."""
    class Meta:
        model = Album
        exclude = ['user', 'date_uploaded', 'date_published', 'published', 'image']
