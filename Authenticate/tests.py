from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Authenticate.models import UserData

class AuthenticateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        
    def test_register_view_get(self):
        response = self.client.get(reverse('Authenticate:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_valid(self):
        response = self.client.post(reverse('Authenticate:register'), {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('Authenticate:login')) 
        
    def test_login_view_get(self):
        response = self.client.get(reverse('Authenticate:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('Authenticate:login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('Homepage:home_section'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('Authenticate:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username atau password salah. Silakan coba lagi.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_redirect_for_staff_user(self):
        staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        response = self.client.post(reverse('Authenticate:login'), {
            'username': 'staffuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Dashboard:main_dashboard'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('Authenticate:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Homepage:home_section'))
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_user_data_model(self):
        user_data = UserData.objects.create(
            user=self.user,
            profile_name="Test User",
            username=self.user.username,
            location="Test City",
            email="test@example.com",
        )
        self.assertEqual(user_data.profile_name, "Test User")
        self.assertEqual(user_data.username, self.user.username)
        self.assertEqual(user_data.email, "test@example.com")
