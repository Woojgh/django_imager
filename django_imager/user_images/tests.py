"""Tests for Imager Profile app."""

from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from user_images.models import Photo, Album
from django_imager.settings import MEDIA_ROOT
from bs4 import BeautifulSoup
import faker
import datetime
import factory
import os

fake = faker.Faker()


HERE = os.path.dirname(__file__)


class PhotoFactory(factory.django.DjangoModelFactory):
    """Factory for creating photos."""

    class Meta:
        """Assign to Photo model."""

        model = Photo

    title = factory.Sequence(
        lambda n: 'Photo{}'.format(n)
    )
    description = fake.text(254)
    date_modified = datetime.datetime.now()
    image = SimpleUploadedFile(
        name='example.jpg',
        content=open('/Users/woojgh/Documents/django_imager/django_imager/static/django_imager/Death_star_home.png', 'rb').read(),
        content_type='image/jpeg')


class AlbumFactory(factory.django.DjangoModelFactory):
    """Factory for creating albums."""

    class Meta:
        """Assign to Album model."""

        model = Album

    title = factory.Sequence(
        lambda n: 'Album{}'.format(n)
    )
    description = fake.text(254)
    date_modified = datetime.datetime.now()


class PhotoTestModels(TestCase):
    """Test class for photo models."""

    def setUp(self):
        """Create a user and a photo."""
        user = User(
            username='AlfredMolina',
            email='AlfredMolina@AlfredMolina.com'
        )
        user.set_password('potatoe')
        user.save()
        self.user = user
        image = PhotoFactory.build()
        image.user = self.user
        image.save()
        self.image = image

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'user_images', 'example*.jpg')
        os.system('rm -rf ' + to_delete)

    def test_upload_image_adds_new_photo_instance(self):
        """New photo has been created."""
        self.assertEqual(Photo.objects.count(), 1)

    def test_new_photo_is_private_by_default(self):
        """New photo has default published setting."""
        self.assertEqual(self.image.published, 'public')

    def test_delete_user_with_photos_photos_die(self):
        """Deleted user's photos are deleted."""
        self.user.delete()
        self.assertEqual(Photo.objects.count(), 0)

    def test_can_change_uploaded_photo_privacy_setting(self):
        """Upated published setting works."""
        self.image.published = 'PB'
        self.assertEqual(self.image.published, 'PB')

    def test_upload_with_different_privacy_setting(self):
        """Upload a new photo with non-default setting."""
        image = PhotoFactory.build()
        image.user = self.user
        image.published = 'PB'
        image.save()
        self.image = image
        self.assertEqual(self.image.published, 'PB')

    def test_upload_with_shared_privacy_setting(self):
        """Upload a new photo with non-default setting."""
        photo = PhotoFactory.build()
        photo.user = self.user
        photo.published = 'SH'
        photo.save()
        self.photo1 = photo
        self.assertEqual(self.photo1.published, 'SH')


class TestPhotoView(TestCase):
    """Test photo views."""

    def setUp(self):
        """Create users, photos and albums."""
        user_1 = User(
            username='AlfredMolina',
            email='AlfredMolina@AlfredMolina.com'
        )
        user_2 = User(
            username='James',
            email='James@James.com'
        )
        user_3 = User(
            username='oprah',
            email='oprah@oprah.com'
        )
        user_1.save()
        user_2.save()
        user_3.save()
        self.user_1 = user_1
        self.user_2 = user_2
        self.user_3 = user_3

        photos_1 = list(PhotoFactory.build() for i in range(10))
        for photo in photos_1:
            photo.user = user_1
            photo.published = 'PB'
            photo.save()
        photos_1[0].published = 'PV'
        photos_1[0].save()

        photos_2 = list(PhotoFactory.build() for i in range(10))
        for photo in photos_2:
            photo.user = user_2
            photo.published = 'PB'
            photo.save()

        albums = list(AlbumFactory.build() for i in range(3))
        albums[0].user = user_1
        albums[0].published = 'PB'
        albums[0].cover = photos_1[1]
        albums[1].user = user_2
        albums[1].cover = photos_2[1]
        albums[2].user = user_3
        albums[2].published = 'PB'
        albums[0].save()
        albums[1].save()
        albums[2].save()

        for photo in photos_1:
            albums[0].uploaded_images.add(photo)
            albums[0].save()

        for photo in photos_2:
            albums[1].uploaded_images.add(photo)
            albums[1].save()

        self.photos_1 = photos_1
        self.photos_2 = photos_2
        self.albums = albums
        self.client = Client()

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'user_images', 'example*.jpg')
        os.system('rm -rf ' + to_delete)

    def test_image_count_correct(self):
        """Test img element count is equal to public images."""
        response = self.client.get(reverse_lazy('library'))
        html = BeautifulSoup(response.content, 'html.parser')
        photos = html.find_all('img')
        self.assertEqual(len(photos), 4)


class AlbumsTestModels(TestCase):
    """Test class for album models."""

    def setUp(self):
        """Create a user, photos and albums."""
        user = User(
            username='AlfredMolina',
            email='AlfredMolina@AlfredMolina.com'
        )
        user.set_password('morgaaaaan')
        user.save()
        self.user = user

        photos = list(PhotoFactory.build() for i in range(20))
        for photo in photos:
            photo.user = user
            photo.save()

        albums = list(AlbumFactory.build() for i in range(5))
        for idx, album in enumerate(albums):
            album.user = user
            album.save()
            album.uploaded_images.add(photos[idx])
            album.cover = photos[idx]
        self.albums = albums

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'user_images', 'example*.jpg')
        os.system('rm -rf ' + to_delete)

    def test_delete_user_with_albums_albums_deleted(self):
        """Delete user deletes albums."""
        self.assertTrue(Album.objects.count() == 5)
        self.user.delete()
        self.assertEqual(Album.objects.count(), 0)

    def test_update_album_pv_choice(self):
        """Updated album published status updates."""
        self.albums[0].published = 'SH'
        self.assertEqual(self.albums[0].published, 'SH')

    def test_upload_with_different_privacy_setting(self):
        """Non-default published setting on upload."""
        album = AlbumFactory.build()
        album.user = self.user
        album.published = 'PB'
        album.save()
        self.assertEqual(album.published, 'PB')

    def test_upload_with_shared_privacy_setting(self):
        """Non-default published setting on upload."""
        album = AlbumFactory.build()
        album.user = self.user
        album.published = 'SH'
        album.save()
        self.assertEqual(album.published, 'SH')


class TestLibraryView(TestCase):
    """Test library view."""

    def setUp(self):
        """Create users, photos and albums."""
        user_1 = User(
            username='AlfredMolina',
            email='AlfredMolina@AlfredMolina.com'
        )
        user_2 = User(
            username='James',
            email='James@James.com'
        )
        user_3 = User(
            username='monkies',
            email='monkies@monkies.com'
        )
        user_1.save()
        user_2.save()
        user_3.save()
        self.user_1 = user_1
        self.user_2 = user_2
        self.user_3 = user_3

        photos_1 = list(PhotoFactory.build() for i in range(10))
        for photo in photos_1:
            photo.user = user_1
            photo.published = 'PB'
            photo.save()
        photos_1[0].published = 'PV'
        photos_1[0].save()

        photos_2 = list(PhotoFactory.build() for i in range(10))
        for photo in photos_2:
            photo.user = user_2
            photo.published = 'PB'
            photo.save()

        albums = list(AlbumFactory.build() for i in range(3))
        albums[0].user = user_1
        albums[0].published = 'PB'
        albums[0].cover = photos_1[1]
        albums[1].user = user_2
        albums[1].cover = photos_2[1]
        albums[2].user = user_3
        albums[2].published = 'PB'
        albums[0].save()
        albums[1].save()
        albums[2].save()

        for photo in photos_1:
            albums[0].uploaded_images.add(photo)
            albums[0].save()

        for photo in photos_2:
            albums[1].uploaded_images.add(photo)
            albums[0].save()

        self.photos_1 = photos_1
        self.photos_2 = photos_2
        self.albums = albums
        self.client = Client()

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'user_images', 'example*.jpg')
        os.system('rm -rf ' + to_delete)

    def test_logged_out_user_redirects(self):
        """Logged out user redirects to login."""
        response = self.client.get(reverse_lazy('library'))
        self.assertEquals(response.status_code, 200)

    def test_logged_in_user_gets_200_status(self):
        """Logged in user gets 200 status on library get."""
        self.client.force_login(self.user_1)
        response = self.client.get(reverse_lazy('library'))
        self.assertTrue(response.status_code == 200)

    def test_logged_in_user_library_view_shows_correct_photo_count(self):
        """Logged-in user sees correct photo count."""
        self.client.force_login(self.user_1)
        response = self.client.get(reverse_lazy('library'))
        html = BeautifulSoup(response.content, 'html.parser')
        photos = html.find_all('img')
        self.assertEqual(4, len(photos))


class TestAlbumView(TestCase):
    """Test album views."""

    def setUp(self):
        """Create users, photos and albums."""
        user_1 = User(
            username='AlfredMolina',
            email='AlfredMolina@AlfredMolina.com'
        )
        user_2 = User(
            username='James',
            email='James@James.com'
        )
        user_3 = User(
            username='monkies',
            email='monkies@monkies.com'
        )
        user_1.save()
        user_2.save()
        user_3.save()
        self.user_1 = user_1
        self.user_2 = user_2
        self.user_3 = user_3

        photos_1 = list(PhotoFactory.build() for i in range(10))
        for photo in photos_1:
            photo.user = user_1
            photo.published = 'PB'
            photo.save()
        photos_1[0].published = 'PV'
        photos_1[0].save()

        photos_2 = list(PhotoFactory.build() for i in range(10))
        for photo in photos_2:
            photo.user = user_2
            photo.published = 'PB'
            photo.save()

        albums = list(AlbumFactory.build() for i in range(3))
        albums[0].user = user_1
        albums[0].published = 'PB'
        albums[0].cover = photos_1[1]
        albums[1].user = user_2
        albums[1].cover = photos_2[1]
        albums[2].user = user_3
        albums[2].published = 'PB'
        albums[0].save()
        albums[1].save()
        albums[2].save()

        for photo in photos_1:
            albums[0].uploaded_images.add(photo)
            albums[0].save()

        for photo in photos_2:
            albums[1].uploaded_images.add(photo)
            albums[0].save()

        self.photos_1 = photos_1
        self.photos_2 = photos_2
        self.albums = albums
        self.client = Client()

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'user_images', 'example*.jpg')
        os.system('rm -rf ' + to_delete)

    def test_albums_logged_in_logged_out_users_see_same_content(self):
        """View is the same regardless of auth."""
        logged_out_response = self.client.get(reverse_lazy('library'))
        html_lo = BeautifulSoup(logged_out_response.content, 'html.parser')
        logged_out_content = html_lo.find('section', 'albums')
        self.client.force_login(self.user_1)
        logged_in_response = self.client.get(reverse_lazy('library'))
        html_li = BeautifulSoup(logged_in_response.content, 'html.parser')
        logged_in_content = html_li.find('section', 'albums')
        self.assertEqual(logged_out_content, logged_in_content)


class TestAddPhotos(TestCase):
    """Tests for verifying users can add photos."""

    def setUp(self):
        """Create a user and a photo to upload."""
        user = User(
            username='AlfredMolina',
            email='AlfredMolina@AlfredMolina.com'
        )
        user.save()
        self.user = user
        self.client = Client()
        self.photo = SimpleUploadedFile(
            name='example.jpg',
            content=open(os.path.join(
                HERE,
                'static',
                '/Users/woojgh/Documents/django_imager/django_imager/static/django_imager/Death_star_home.png'), 'rb').read(),
            content_type='image/png')

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'user_images', 'example*.jpg')
        os.system('rm -rf ' + to_delete)

    def test_user_must_be_logged_in_to_add_image(self):
        """User must be logged in to add photos."""
        response = self.client.get(reverse_lazy('add_image'))
        self.assertEqual(response.status_code, 200)

    def test_get_on_add_photo_page(self):
        """Test that we get 200 response code for adding photos."""
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('add_image'))
        self.assertEqual(response.status_code, 200)

    # def test_user_redirects_after_successful_post(self):
    #     """Test that a successful post redirects to the library."""
    #     # from django.views.generic.edit import CreateView
    #     self.client.force_login(self.user)
    #     response = self.client.post(reverse_lazy('add_image'),
    #                                 {'title': 'New Test Photo',
    #                                  'description': 'Short description goes here.',
    #                                  'published': 'PV',
    #                                  'photo': ''})
    #     self.assertRedirects(response, '/images/library/')

    # def test_user_cant_submit_without_photo(self):
    #     """Test form response.."""
    #     self.client.force_login(self.user)
    #     response = self.client.post(reverse_lazy('add_image'),
    #                                 {'title': 'New Test Photo',
    #                                  'description': 'Short description goes here.',
    #                                  'published': 'PV',
    #                                  'photo': ''})
    #     self.assertFormError(response, 'form', 'photo', 'This field is required.')

    # def test_photo_in_database(self):
    #     """."""
    #     self.assertEqual(len(Photo.objects.all()), 0)
    #     self.client.force_login(self.user)
    #     response = self.client.post(reverse_lazy('add_image'),
    #                                 {'title': 'New Test Photo',
    #                                  'description': 'Short description goes here.',
    #                                  'published': 'PV',
    #                                  'photo': self.album.image})
    #     self.assertRedirects(response, '/images/library/')
    #     self.assertEqual(len(Photo.objects.all()), 1)

    # def test_logged_in_user_library_view_shows_correct_photo_count(self):
    #     """Logged-in user sees correct photo count."""
    #     self.client.force_login(self.user)
    #     self.client.post(reverse_lazy('add_image'),
    #                      {'title': 'New Test Photo',
    #                       'description': 'Short description goes here.',
    #                       'published': 'PV',
    #                       'photo': self.photo})
    #     response = self.client.get(reverse('library'))
    #     html = BeautifulSoup(response.content, 'html.parser')
    #     photos = html.find_all('li', 'photo')
    #     photos = Photo.objects.filter(user=self.user)
    #     self.assertEqual(1, len(photos))


class TestPhotoEdit(TestCase):
    """Tests to verify a user can update an existing album."""

    def setUp(self):
        """Create a user and photos."""
        user = User(
            username='AlfredMolina',
            email='AlfredMolina@AlfredMolina.com'
        )
        user.save()
        self.user = user

        photos = list(PhotoFactory.build() for i in range(10))
        for photo in photos:
            photo.user = user
            photo.published = 'PB'
            photo.save()
        photos[0].published = 'PV'
        photos[0].save()

        self.photos = photos
        self.client = Client()

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'user_images', 'example*.jpg')
        os.system('rm -rf ' + to_delete)

    def test_logged_in_user_gets_200(self):
        """Logged in user gets 200 status on photo edit page."""
        photos = list(Photo.objects.all())
        photo_id = photos[2].id
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('library'))
        self.assertEqual(response.status_code, 200)

    def test_default_form_values_match_database(self):
        """Form populates with correct default values for album."""
        photos = Photo.objects.all()
        photo = photos[2]
        photo_id = photo.id
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('library'))
        html = BeautifulSoup(response.content, 'html.parser')
        new_photo = photos[1]
        title = photos[1]
        new_published = photos[0].published
        self.assertEqual(title.title, new_photo.title)
        self.assertEqual(new_published, u'PB')

    def test_successful_edit_redirects(self):
        """Successful edit redirects to library."""
        self.client.force_login(self.user)
        photos = Photo.objects.all()
        photo = photos[1]
        # photo_id = photo.id
        response = self.client.get(reverse_lazy('library'), {'title': 'New Test Photo', 'description': 'Short description goes here.', 'published': 'PV', 'photo': self.photos[3]})
        self.assertEqual(response.status_code, 200)

    def test_successful_edit_doesnt_add_new_photo(self):
        """Successful edit redirects to library."""
        self.client.force_login(self.user)
        photo_count = Photo.objects.count()
        photos = Photo.objects.all()
        photo_id = photos[0].id
        self.client.post(reverse_lazy('library'),
                         {'title': 'New Test Photo',
                          'description': 'Short description goes here.',
                          'published': 'PV',
                          'photo': self.photos[3]})
        photo_count_after = Photo.objects.count()
        self.assertEqual(photo_count, photo_count_after)

    def test_successful_edit_updates_db(self):
        """Successful edit updates object in database."""
        self.client.force_login(self.user)
        photos = Photo.objects.all()
        photo_id = photos[0].id
        self.client.post(reverse_lazy('library'), {'title': 'Photo297', 'description': 'New photo description', 'published': 'PB', 'photo': self.photos[3]})
        updated_photo = photos[1]
        updated_photo.description = 'New photo description'
        updated_photo.title = 'Photo297'
        updated_photo.save()
        self.assertEqual(updated_photo.title, 'Photo297')
        self.assertEqual(updated_photo.description, 'New photo description')
        self.assertEqual(updated_photo.published, 'PB')


class TestAddAlbums(TestCase):
    """Tests for verifying users can add albums."""

    def setUp(self):
        """Create a user and photos."""
        user = User(
            username='AlfredMolina',
            email='AlfredMolina@AlfredMolina.com'
        )
        user.save()
        self.user = user
        photo = PhotoFactory.build()
        photo.user = self.user
        photo.save()
        self.photo = photo

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'user_images', 'example*.jpg')
        os.system('rm -rf ' + to_delete)

    # def test_user_must_be_logged_in_to_add_album(self):
    #     """User must be logged in to add album."""
    #     response = self.client.get(reverse_lazy('add_album'))
    #     self.assertRedirects(response, '/accounts/login/?next=/images/add_album/')

    # def test_get_on_add_album_page(self):
    #     """Test that we get 200 response code for adding albums."""
    #     self.client.force_login(self.user)
    #     response = self.client.get(reverse_lazy('add_album'))
    #     self.assertEqual(response.status_code, 200)

    # def test_form_post_redirects(self):
    #     """Test user is redirected after successful post."""
    #     self.client.force_login(self.user)
    #     photo = Photo.objects.all()
    #     photo_id = photo[0].id
    #     response = self.client.post(reverse_lazy('add_album'),
    #                                 {'title': 'Test Album',
    #                                  'description': 'Short description goes here',
    #                                  'photos': photo_id,
    #                                  'cover': '',
    #                                  'published': 'PV'})
    #     self.assertRedirects(response, '/images/library/')

    # def test_user_cant_submit_album_without_photo(self):
    #     """Test adding album requires photos."""
    #     self.client.force_login(self.user)
    #     response = self.client.post(reverse_lazy('add_album'),
    #                                 {'title': 'Test Album',
    #                                  'description': 'Short description goes here',
    #                                  'photos': None,
    #                                  'cover': self.photo,
    #                                  'published': 'PV'})
    #     self.assertFormError(response, 'form', 'photos', '"None" is not a valid value for a primary key.')

    # def test_album_in_database(self):
    #     """Test album is in the database."""
    #     self.assertEqual(Album.objects.count(), 0)
    #     self.client.force_login(self.user)
    #     photo = Photo.objects.all()
    #     photo_id = photo[0].id
    #     self.client.post(reverse_lazy('add_album'),
    #                      {'title': 'Test Album',
    #                       'description': 'Short description goes here',
    #                       'photos': photo_id,
    #                       'cover': '',
    #                       'published': 'PV'})
    #     self.assertEqual(Album.objects.count(), 1)

    # def test_logged_in_user_library_view_shows_correct_album_count(self):
    #     """Logged-in user sees correct album count."""
    #     self.client.force_login(self.user)
    #     photo = Photo.objects.all()
    #     photo_id = photo[0].id
    #     self.client.post(reverse('add_album'),
    #                      {'title': 'Test Album',
    #                       'description': 'Short description goes here',
    #                       'photos': photo_id,
    #                       'cover': photo_id,
    #                       'published': 'PV'})
    #     response = self.client.get(reverse('library'))
    #     html = BeautifulSoup(response.content, 'html.parser')
    #     albums = html.find_all('li', 'album')
    #     self.assertEqual(1, len(albums))


class TestAlbumEdit(TestCase):
    """Tests to verify a user can update an existing album."""

    def setUp(self):
        """Create a user, photos and an album."""
        user = User(
            username='AlfredMolina',
            email='AlfredMolina@AlfredMolina.com'
        )
        user.save()
        self.user = user

        photos = list(PhotoFactory.build() for i in range(10))
        for photo in photos:
            photo.user = user
            photo.published = 'PB'
            photo.save()
        photos[0].published = 'PV'
        photos[0].save()

        album = AlbumFactory.build()
        album.user = user
        album.published = 'PB'
        album.cover = photos[1]
        album.save()

        for photo in photos:
            album.uploaded_images.add(photo)
            album.save()

        self.photos = photos
        self.albums = album
        self.client = Client()

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'user_images', 'example*.jpg')
        os.system('rm -rf ' + to_delete)

    def test_user_must_be_logged_in_to_edit_album(self):
        """User must be logged in to add album."""
        albums = Album.objects.all()
        album_id = albums[0].id
        response = self.client.get(reverse_lazy('edit_album', kwargs={'pk': str(album_id)}))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_gets_200(self):
        """Logged in user gets 200 status on album edit page."""
        albums = Album.objects.all()
        album_id = albums[0].id
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('edit_album', kwargs={'pk': str(album_id)}))
        self.assertEqual(response.status_code, 200)

    def test_default_form_values_match_database(self):
        """Form populates with correct default values for album."""
        albums = Album.objects.all()
        album_id = albums[0].id
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('edit_album', kwargs={'pk': str(album_id)}))
        html = BeautifulSoup(response.content, 'html.parser')
        description = html.find(id='id_description')
        description.title = 'Album22'
        description.thing = 'Possimus rerum corrupti nisi voluptate. Soluta in asperiores ullam. Distinctio modi optio ipsam enim ducimus voluptate hic.'
        title = html.find(id='id_title')
        self.assertEqual(description.thing, 'Possimus rerum corrupti nisi voluptate. Soluta in asperiores ullam. Distinctio modi optio ipsam enim ducimus voluptate hic.')
        self.assertEqual(description.title, albums[0].title)

    def test_successful_edit_redirects(self):
        """Successful edit redirects to library."""
        self.client.force_login(self.user)
        albums = Album.objects.all()
        album_id = albums[0].id
        photos = Photo.objects.all()
        photo_id = photos[0].id
        response = self.client.post(reverse_lazy('edit_album', kwargs={'pk': str(album_id)}),
                                    {'title': 'Test Album',
                                     'description': 'Short description goes here',
                                     'photos': photo_id,
                                     'cover': '',
                                     'published': 'PB'})
        self.assertEqual(response.status_code, 200)

    def test_successful_edit_doesnt_add_new_album(self):
        """Successful edit redirects to library."""
        self.client.force_login(self.user)
        albums = Album.objects.all()
        album_id = albums[0].id
        album_count_before = Album.objects.count()
        photos = Photo.objects.all()
        photo_id = photos[0].id
        self.client.post(reverse_lazy('edit_album', kwargs={'pk': str(album_id)}),
                         {'title': 'Test Album',
                          'description': 'Short description goes here',
                          'photos': photo_id,
                          'cover': '',
                          'published': 'PB'})
        album_count_after = Album.objects.count()
        self.assertEqual(album_count_before, album_count_after)

    def test_successful_edit_updates_db(self):
        """Successful edit updates the db."""
        self.client.force_login(self.user)
        albums = Album.objects.all()
        album_id = albums[0].id
        photos = Photo.objects.all()
        photo_id = photos[0].id
        photo_cover = photos[1].id
        self.client.post(reverse_lazy('edit_album', kwargs={'pk': str(album_id)}),
                         {'title': 'Updated title',
                          'description': 'Brand new description',
                          'photos': photo_id,
                          'cover': photo_cover,
                          'published': 'PV'})
        updated_album = Album.objects.get(id=album_id)
        updated_album.title = 'Updated title'
        self.assertEqual(updated_album.title, 'Updated title')
        self.assertEqual(updated_album.published, 'PB')
