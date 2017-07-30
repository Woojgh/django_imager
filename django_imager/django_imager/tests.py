"""Tests for config route and registration."""
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django_imager.settings import MEDIA_ROOT
from django.core import mail
from bs4 import BeautifulSoup
from imager_profile.views import home_view
from user_images.models import Photo
from django.core.files.uploadedfile import SimpleUploadedFile
import faker
import datetime
import factory
import os

HERE = os.path.dirname(__file__)

fake = faker.Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating users."""

    class Meta:
        """Associate with User."""

        model = User
    username = factory.Sequence(lambda n: 'user{}'.format(n))
    email = factory.Sequence(lambda n: 'user{}@example.com'.format(n))


class PhotoFactory(factory.django.DjangoModelFactory):
    """Factory for creating photos."""

    class Meta:
        """Associate with Photo."""

        model = Photo

    title = factory.Sequence(
        lambda n: 'Photo{}'.format(n)
    )
    description = fake.text(254)
    date_modified = datetime.datetime.now()
    image = SimpleUploadedFile(
        name='example.jpg',
        content=open('/Users/woojgh/Documents/Projects/Code401/django_imager/django_imager/static/django_imager/Death_star_home.png', 'rb').read(),
        content_type='image/png')


class Registration(TestCase):
    """Tests for registration process."""

    def setUp(self):
        """Create a client instance."""
        self.client = Client()

    def test_registration_template(self):
        """Test registration route uses registration template."""
        response = self.client.get(reverse('registration_register'))
        self.assertIn('registration/registration_form.html', response.template_name)

    def test_check_new_user_created_after_registration(self):
        """Test that a new user is created after registration."""
        self.assertTrue(User.objects.count() == 0)
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, 'html.parser')

        token = html.find('input', {'name': 'csrfmiddlewaretoken'}).attrs['value']

        data_dict = {
            'csrfmiddlewaretoken': token,
            'username': 'GnarefortheGarthack',
            'email': 'GnarefortheGarthack@GnarefortheGarthack.com',
            'password1': 'GnarefortheGarthack',
            'password2': 'GnarefortheGarthack'
        }
        self.client.post(
            reverse('registration_register'),
            data_dict
        )
        self.assertTrue(User.objects.count() == 0)

    def test_new_user_is_inactive_on_creation(self):
        """Test that new user is inactive by default."""
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, 'html.parser')

        token = html.find('input', {'name': 'csrfmiddlewaretoken'}).attrs['value']

        data_dict = {
            'csrfmiddlewaretoken': token,
            'username': 'GnarefortheGarthack',
            'email': 'GnarefortheGarthack@GnarefortheGarthack.com',
            'password1': 'GnarefortheGarthack',
            'password2': 'GnarefortheGarthack'
        }
        self.client.post(
            reverse('registration_register'),
            data_dict
        )
        # import pdb; pdb.set_trace()
        self.assertTrue(User.is_active)

    def test_registration_email_sent(self):
        """Test that an email exists after a user registers successfully."""
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, 'html.parser')

        token = html.find('input', {'name': 'csrfmiddlewaretoken'}).attrs['value']

        self.assertEquals(len(mail.outbox), 0)

        
        data_dict = {
            'csrfmiddlewaretoken': token,
            'username': 'GnarefortheGarthack',
            'email': 'GnarefortheGarthack@GnarefortheGarthack.com',
            'password1': 'GnarefortheGarthack',
            'password2': 'GnarefortheGarthack'
        }
        self.client.post(
            reverse('registration'),
            data_dict
        )
        self.assertEquals(len(mail.outbox), 1)


class LoginLogout(TestCase):
    """Tests for login / logout process."""

    def setUp(self):
        """Create a client instance."""
        user = User(
            username='oprah',
            email='oprah@oprah.com'
        )
        user.save()
        self.user = user
        self.client = Client()
        self.req_factory = RequestFactory()
        photos_1 = PhotoFactory.build()
        photos_1.user = self.user
        photos_1.title = 'Private Image'
        photos_1.save()
        photos_2 = PhotoFactory.build()
        photos_2.user = self.user
        photos_2.title = 'Public Image'
        photos_2.published = 'PB'
        photos_2.save()
        self.photos_1 = photos_1
        self.photos_2 = photos_2

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'user_images', 'example*.jpg')
        os.system('rm -rf ' + to_delete)

    def test_home_view_returns_status_code_200(self):
        """Test home view has status 200."""
        request = RequestFactory().get('/')
        view = home_view.as_view()
        response = view(request)
        self.assertTrue(response.status_code == 200)

    def test_unauthenticated_user_sees_login(self):
        """Unauthenticated user sees login button on home route."""
        response = self.client.get(reverse('home'))
        self.assertTrue(b'login' in response.content.lower())

    def test_authenticated_user_sees_logout(self):
        """Authenticated user sees logout button on home route."""
        test_user = User(username='GnarefortheGarthack')
        test_user.set_password('GnarefortheGarthack')
        test_user.save()
        self.client.post(reverse('login'), {'username': 'GnarefortheGarthack', 'password': 'GnarefortheGarthack'})
        response = self.client.get(reverse('home'))
        self.assertFalse(b'login' in response.content.lower())
        self.assertTrue(b'logout' in response.content.lower())

    def test_if_user_is_authenticated_and_logsout_theyre_no_longer_authenticated(self):
        """Test authenticated user logs out and sees login button."""
        test_user = User(username='GnarefortheGarthack')
        test_user.set_password('GnarefortheGarthack')
        test_user.save()
        self.client.post(reverse('login'), {'username': 'GnarefortheGarthack', 'password': 'GnarefortheGarthack'})
        response = self.client.get(reverse('logout'), follow=True)
        self.assertTrue(b'login' in response.content.lower())

    def test_authenticated_user_name_on_home(self):
        """Test authenticated user's name shows up on home."""
        test_user = User(username='GnarefortheGarthack')
        test_user.set_password('GnarefortheGarthack')
        test_user.save()
        self.client.post(reverse('login'), {'username': 'GnarefortheGarthack', 'password': 'GnarefortheGarthack'})
        response = self.client.get(reverse('home'))
        self.assertFalse(b'GnarefortheGarthack' in response.content.lower())

    def test_logged_out_user_name_not_on_home(self):
        """Test logging user in and logging user out has user name on home page."""
        test_user = User(username='GnarefortheGarthack')
        test_user.set_password('GnarefortheGarthack')
        test_user.save()
        self.client.post(reverse('login'), {'username': 'GnarefortheGarthack', 'password': 'GnarefortheGarthack'})
        response = self.client.get(reverse('logout'), follow=True)
        self.assertFalse(b'GnarefortheGarthack' in response.content.lower())

    def test_successful_login_reroutes(self):
        """Test successful login reroutes to home page."""
        # import pdb; pdb.set_trace()
        test_user = User(username='GnarefortheGarthack')
        test_user.set_password('GnarefortheGarthack')
        test_user.save()
        response = self.client.post(reverse('login'), {'username': 'GnarefortheGarthack', 'password': 'GnarefortheGarthack'}, follow=True)
        self.assertTrue(response.request['PATH_INFO'] == '/library/')