from django.test import TestCase
from django.urls import reverse
from ServiceCenter.models import ServiceCenter
from ServiceCenter.forms import ServiceForm
from django.contrib.auth.models import User
from Authenticate.models import UserData

class ServiceCenterModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.user_data = UserData.objects.create(
            user=self.user,
            profile_name="test user",
            username="testuser"
        )
        self.service_center = ServiceCenter.objects.create(
            user=self.user_data,
            name="coba-coba test service",
            address="123 test alamat benar",
            contact="1234567890",
            rating=4.5,
            total_reviews=10
        )

    def test_service_center_creation(self):
        self.assertEqual(self.service_center.name, "coba-coba test service")

class ServiceCenterViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user_data = UserData.objects.create(
            user=self.user,
            profile_name="Test User",
            username="testuser"
        )
        self.service_center = ServiceCenter.objects.create(
            user=self.user_data,
            name="coba-coba test service",
            address="123 test alamat benar",
            contact="1234567890",
            rating=4.5,
            total_reviews=10
        )

    def test_show_service_page(self):
        response = self.client.get(reverse('ServiceCenter:show_service_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service_page.html')

    def test_create_service_center(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('ServiceCenter:create_service_center'), {
            'name': 'coba-coba test service 2',
            'address': '456 test alamat benar',
            'contact': '0987654321',
            'rating': 4.0,
            'total_reviews': 5,
        })
        self.assertEqual(response.status_code, 302)
        
    def test_add_service_center_ajax(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('ServiceCenter:add_service_center_ajax'), {
            'name': 'coba-coba test service 2',
            'address': '456 test alamat benar',
            'contact': '0987654321',
            'rating': 4.0,
            'total_reviews': 5,
        })
        self.assertEqual(response.status_code, 201)
    
    def test_show_json(self):
        response = self.client.get(reverse('ServiceCenter:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.service_center.name, response.content.decode())

    def test_show_xml(self):
        response = self.client.get(reverse('ServiceCenter:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.service_center.name, response.content.decode())

class ServiceCenterFormsTest(TestCase):
    def test_service_form_valid(self):
        form = ServiceForm(data={
            'name': 'coba-coba test service',
            'address': '456 test alamat benar',
            'contact': '1234567890',
            'rating': 4.5,
            'total_reviews': 10,
        })
        self.assertTrue(form.is_valid())

    def test_service_form_invalid(self):
        form = ServiceForm(data={
            'name': '',
            'address': '456 test alamat salah',
            'contact': '1234567890',
            'rating': 4.5,
            'total_reviews': 10,
        })
        self.assertFalse(form.is_valid())
