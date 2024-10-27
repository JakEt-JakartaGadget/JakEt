from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Homepage.models import Phone
import uuid
from CustomerService.models import Chat
from django.utils import timezone

class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)
        self.regular_user = User.objects.create_user(username='regularuser', password='password', is_staff=False)
        self.phone = Phone.objects.create(
            brand="Apple", model="iPhone 13", storage="128GB", ram="4GB",
            screen_size_inches=6.1, camera_mp="12MP", battery_capacity_mAh=3240,
            price_usd=799, price_inr=59000, rating=4, image_url="https://example.com/image.jpg"
        )

    def test_dashboard_access_staff_user(self):
        self.client.login(username='staffuser', password='password')
        response = self.client.get(reverse('Dashboard:main_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertIn('products', response.context)

    def test_add_product_view_get(self):
        self.client.login(username='staffuser', password='password')
        response = self.client.get(reverse('Dashboard:add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_form.html')
        self.assertIn('form', response.context)

    def test_edit_product_view_get(self):
        self.client.login(username='staffuser', password='password')
        response = self.client.get(reverse('Dashboard:edit_product', args=[self.phone.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_form.html')
        self.assertIn('form', response.context)

    def test_delete_product_view(self):
        self.client.login(username='staffuser', password='password')
        response = self.client.post(reverse('Dashboard:delete_product', args=[self.phone.id]))
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(Phone.objects.filter(id=self.phone.id).exists())

class ChatDashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
        self.regular_user = User.objects.create_user(username='user', password='user123', email='user@example.com')
        self.chat = Chat.objects.create(user=self.regular_user, message='Hello', date=timezone.now(), time_sent=timezone.now())

    def test_chat_dashboard_superuser_access(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('Dashboard:chat_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customerservice-dashboard.html')
        self.assertIn('users_with_chats', response.context)

    def test_chat_dashboard_regular_user_access(self):
        self.client.login(username='user', password='user123')
        response = self.client.get(reverse('Dashboard:chat_dashboard'))
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'error': 'Unauthorized'})

    def test_chat_dashboard_users_with_chats(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('Dashboard:chat_dashboard'))
        self.assertEqual(response.status_code, 200)
        users_with_chats = response.context['users_with_chats']
        self.assertEqual(len(users_with_chats), 1)
        self.assertEqual(users_with_chats[0].username, 'user')
        self.assertEqual(users_with_chats[0].unread_messages, 1)
        self.assertEqual(users_with_chats[0].last_chat, 'Hello')

