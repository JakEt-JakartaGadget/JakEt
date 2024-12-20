from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Discussion, Reply
import json
import uuid

User = get_user_model()

class ForumViewTests(TestCase):
    def setUp(self):
        # Create a test user and log them in
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.client.login(username='testuser', password='password')

        # Create a sample discussion
        self.discussion = Discussion.objects.create(owner=self.user, topic="Sample Topic")
        
    def test_forum_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('UserForum:forum'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user-forum.html')

    def test_add_discussion_success(self):
        # Test adding a discussion successfully
        response = self.client.post(reverse('UserForum:add_discussion'), {'topic': 'New Discussion Topic'})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['topic'], 'New Discussion Topic')

    def test_add_discussion_failure(self):
        # Test adding a discussion with an empty topic
        response = self.client.post(reverse('UserForum:add_discussion'), {'topic': ''})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data['success'])

    def test_add_discussion_no_topic(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('UserForum:add_discussion'), {'topic': ''})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False})

    def test_delete_discussion_success(self):
        # Test deleting a discussion as a superuser
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('UserForum:delete_discussion', args=[self.discussion.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_discussion_view(self):
        # Test viewing a single discussion
        response = self.client.get(reverse('UserForum:discussion_view', args=[self.discussion.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussion.html')
        self.assertEqual(response.context['discussion'], self.discussion)

    def test_send_reply_success(self):
        # Test sending a reply to a discussion
        data = {
            'message': 'This is a test reply.'
        }
        response = self.client.post(
            reverse('UserForum:send_reply', args=[self.discussion.id]),
            json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message']['message'], 'This is a test reply.')
        self.assertEqual(response_data['message']['sender']['username'], 'testuser')

    def test_send_reply_discussion_not_found(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('UserForum:send_reply', args=[uuid.uuid4()]), json.dumps({'message': 'New Reply'}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'Discussion not found'})