from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from CustomerService.models import Chat, DailyCustomerService
import json
from django.utils import timezone

User  = get_user_model()

class CustomerServiceTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a DailyCustomerService instance for today's date
        self.daily_service = DailyCustomerService.objects.create(user=self.user, date=timezone.now().date())

    def test_customer_service_view(self):
        # Create a Chat instance
        Chat.objects.create(user=self.user, message='Test message')
        
        response = self.client.get(reverse('CustomerService:customer_service'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer-service.html')
        self.assertContains(response, 'grouped_chats')

    def test_send_message_view(self):
        url = reverse('CustomerService:send_message')
        message_data = json.dumps({'message': 'Hello, this is a test message.'})

        response = self.client.post(url, message_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('status', response_data)
        self.assertEqual(response_data['status'], 'success')

        # Check if the message was created correctly
        chat = Chat.objects.get(id=response_data['message']['id'])
        self.assertEqual(chat.message, 'Hello, this is a test message.')
        self.assertEqual(chat.time_sent.strftime('%H:%M'), response_data['message']['time'])
        self.assertEqual(chat.date.strftime('%Y-%m-%d'), response_data['message']['date'])

    def test_send_message_view_invalid_data(self):
        url = reverse('CustomerService:send_message')
        invalid_message_data = json.dumps({'message': ''})

        response = self.client.post(url, invalid_message_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'Invalid request'})

    def test_get_messages_view(self):
        chat = Chat.objects.create(user=self.user, message='First message')
        url = reverse(' CustomerService:get_messages')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data['messages']), 1)
        self.assertEqual(response_data['messages'][0]['id'], chat.id)
        self.assertEqual(response_data['messages'][0]['message'], chat.message)
        self.assertEqual(response_data['messages'][0]['time'], chat.time_sent.strftime('%H:%M'))
        self.assertEqual(response_data['messages'][0]['date'], chat.date.strftime('%Y-%m-%d'))

    def test_get_messages_view_after_timestamp(self):
        chat1 = Chat.objects.create(user=self.user, message='First message')
        chat2 = Chat.objects.create(user=self.user, message='Second message')
        url = reverse('CustomerService:get_messages') + '?after={}'.format(chat1.time_sent.strftime('%H:%M:%S'))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data['messages']), 1)
        self.assertEqual(response_data['messages'][0]['id'], chat2.id)
        self.assertEqual(response_data['messages'][0]['message'], chat2.message)
        self.assertEqual(response_data['messages'][0]['time'], chat2.time_sent.strftime('%H:%M'))
        self.assertEqual(response_data['messages'][0]['date'], chat2.date.strftime('%Y-%m-%d'))