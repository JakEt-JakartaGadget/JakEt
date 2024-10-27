from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Authenticate.models import UserData
from Profile.forms import ProfileForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError

class UserDataModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_data = UserData.objects.create(
            user=self.user,
            profile_name="Test User",
            username="testuser",
            about="This is a test user",
            location="Test City",
            phone="123456789",
            email="testuser@example.com",
            password="password123",
        )

    def test_lst_data(self):
        data = self.user_data.lst_data()
        self.assertEqual(data['profile_name'], "Test User")
        self.assertEqual(data['username'], "testuser")
        self.assertEqual(data['about'], "This is a test user")

    def test_user_data_duplicate_error(self):
        with self.assertRaises(IntegrityError):
            UserData.objects.create(
                user=self.user,
                profile_name="Another User",
                username="anotheruser",
            )

class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_profile_view_with_data(self):
        UserData.objects.create(user=self.user, profile_name="Test User", username="testuser")
        response = self.client.get(reverse('Profile:profile_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_view_without_data(self):
        response = self.client.get(reverse('Profile:profile_view'))
        self.assertRedirects(response, reverse('Profile:create_profile'))

class CreateProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_profile_post(self):
        profile_picture = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(reverse('Profile:create_profile'), {
            'profile_name': 'New User',
            'username': 'newuser',
            'about': 'New about info',
            'phone': '123456789',
            'email': 'newuser@example.com',
            'profile_picture': profile_picture
        })
        self.assertRedirects(response, reverse('Profile:profile_view'))
        user_data = UserData.objects.get(user=self.user)
        self.assertEqual(user_data.profile_name, 'New User')
        self.assertEqual(user_data.username, 'newuser')

    def test_create_profile_existing_data(self):
        UserData.objects.create(user=self.user, profile_name="Existing User", username="testuser")
        response = self.client.get(reverse('Profile:create_profile'))
        self.assertRedirects(response, reverse('Profile:profile_view'))

class EditProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.user_data = UserData.objects.create(user=self.user, profile_name="Test User", username="testuser")

    def test_edit_profile_post(self):
        response = self.client.post(reverse('Profile:edit_profile'), {
            'profile_name': 'Updated User',
            'username': 'updateduser',
            'about': 'Updated info',
            'phone': '987654321',
            'email': 'updated@example.com',
        })
        self.assertRedirects(response, reverse('Profile:profile_view'))
        self.user_data.refresh_from_db()
        self.assertEqual(self.user_data.profile_name, 'Updated User')
        self.assertEqual(self.user_data.username, 'updateduser')

    def test_delete_profile_picture_no_picture(self):
        response = self.client.post(reverse('Profile:delete_profile_picture'))
        self.assertEqual(response.status_code, 404)

    def test_profile_picture_default_display(self):
        self.user_data.profile_picture.delete()
        response = self.client.get(reverse('Profile:profile_view'))
        self.assertContains(response, 'static/image/blank-profile.jpg')

class ProfileFormTests(TestCase):
    def test_form_valid_data(self):
        form = ProfileForm(data={
            'profile_name': 'Valid User',
            'username': 'validuser',
            'about': 'This is valid',
            'phone': '123456789',
            'email': 'validuser@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = ProfileForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_form_required_fields(self):
        form = ProfileForm(data={
            'profile_name': '',
            'username': '',
            'about': '',
            'phone': '',
            'email': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('profile_name', form.errors)
        self.assertIn('username', form.errors)
