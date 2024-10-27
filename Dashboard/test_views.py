from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from CustomerService.models import Chat
from django.utils import timezone

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