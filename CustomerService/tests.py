from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from CustomerService.models import Chat, DailyCustomerService
from datetime import date
import json

User = get_user_model()

class ChatModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_chat_message(self):
        # Create a chat message
        chat_message = Chat.objects.create(
            user=self.user,
            message='Hello, this is a test message.',
            sent_by_user=True
        )
        self.assertEqual(chat_message.message, 'Hello, this is a test message.')
        self.assertEqual(chat_message.user, self.user)
        self.assertFalse(chat_message.read)  # By default, it should not be read

    def test_count_unread_messages(self):
        # Create chat messages
        Chat.objects.create(user=self.user, message='First unread message.')
        Chat.objects.create(user=self.user, message='Second unread message.')
        Chat.objects.create(user=self.user, message='Read message.', read=True)

        # Count unread messages
        unread_count = Chat.count_unread_messages(self.user)
        self.assertEqual(unread_count, 2)

    def test_mark_as_read(self):
        # Create a chat message
        chat_message = Chat.objects.create(user=self.user, message='Message to mark as read.')

        # Mark the message as read
        chat_message.mark_as_read()
        self.assertTrue(chat_message.read)

    def test_mark_as_read_multiple_messages(self):
        # Create multiple chat messages
        message1 = Chat.objects.create(user=self.user, message='First message.')
        message2 = Chat.objects.create(user=self.user, message='Second message.')

        # Mark the first message as read
        message1.mark_as_read()
        self.assertTrue(message1.read)
        self.assertFalse(message2.read)

class DailyCustomerServiceModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_daily_customer_service_creation(self):
        # Create a daily customer service entry
        daily_service = DailyCustomerService.objects.create(user=self.user)

        self.assertEqual(daily_service.user, self.user)
        self.assertEqual(daily_service.date, date.today())

    def test_messages_property(self):
        # Create a daily customer service entry
        daily_service = DailyCustomerService.objects.create(user=self.user)
        
        # Create chat messages for the same date
        Chat.objects.create(user=self.user, message='Message 1', date=daily_service.date)
        Chat.objects.create(user=self.user, message='Message 2', date=daily_service.date)

        # Fetch messages using the property
        messages = daily_service.messages
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].message, 'Message 1')
        self.assertEqual(messages[1].message, 'Message 2')

class CustomerServiceViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.superuser = User.objects.create_superuser(username='admin', password='admin')
        self.chat = Chat.objects.create(user=self.user, message='Hello', sent_by_user=True)

    def test_customer_service_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('customer_service'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer-service.html')
        self.assertIn('grouped_chats', response.context)
        self.assertIn('today', response.context)
        self.assertIn('viewing_user', response.context)

    def test_customer_service_view_as_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('customer_service', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer-service.html')
        self.assertIn('grouped_chats', response.context)
        self.assertIn('today', response.context)
        self.assertIn('viewing_user', response.context)

    def test_send_message_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('send_message'), json.dumps({'message': 'Hi'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['message']['message'], 'Hi')

    def test_send_message_view_as_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('send_message', args=[self.user.id]), json.dumps({'message': 'Hi'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['message']['message'], 'Hi')

    def test_get_messages_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('get_messages'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('messages', response.json())
        self.assertEqual(len(response.json()['messages']), 1)
        self.assertEqual(response.json()['messages'][0]['message'], 'Hello')