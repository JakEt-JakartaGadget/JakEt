from django.test import TestCase, RequestFactory
from django.urls import reverse
from Tiket.models import Tiket
from Tiket.forms import TiketForm
from ServiceCenter.models import ServiceCenter
from django.contrib.auth.models import User
from Authenticate.models import UserData
from datetime import datetime, timedelta

class TiketModelTest(TestCase):
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
        self.tiket = Tiket.objects.create(
            user=self.user_data,
            service_center=self.service_center,
            service_date=datetime.now().date(),
            service_time=datetime.now().time(),
            specific_problems="apa itu masalah"
        )

    def test_tiket_creation(self):
        self.assertEqual(self.tiket.service_center.name, "coba-coba test service")

class TiketViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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
        self.tiket = Tiket.objects.create(
            user=self.user_data,
            service_center=self.service_center,
            service_date=datetime.now().date(),
            service_time=datetime.now().time(),
            specific_problems="apa itu masalah"
        )

    def test_create_tiket(self):
        # Simulate logging in the user
        self.client.login(username='testuser', password='password')
        request = self.factory.post(reverse('Tiket:create_tiket', args=[self.service_center.id]), {
            'service_date': (datetime.now() + timedelta(days=1)).date(),
            'service_time': datetime.now().time(),
            'specific_problems': 'testing masalah 1',
        })
        request.user = self.user
        response = self.client.post(reverse('Tiket:create_tiket', args=[self.service_center.id]), request.POST)
        self.assertEqual(response.status_code, 200)


    def test_reschedule_appointment(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('Tiket:reschedule_appointment', args=[self.tiket.id]), {
            'service_date': (datetime.now() + timedelta(days=2)).date(),
            'service_time': datetime.now().time(),
            'specific_problems': 'apa itu masalah',
        })
        self.assertEqual(response.status_code, 200)
        self.tiket.refresh_from_db()
        self.assertEqual(self.tiket.specific_problems, 'apa itu masalah')

    def test_show_json(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('Tiket:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.tiket.service_center.name, response.content.decode())

    def test_cancel_appointment(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('Tiket:cancel_appointment', args=[self.tiket.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tiket.objects.filter(id=self.tiket.id).exists())

class TiketFormsTest(TestCase):
    def test_tiket_form_invalid(self):
        form = TiketForm(data={
            'service_date': '',
            'service_time': '',
            'specific_problems': 'masalah terakhir',
        })
        self.assertFalse(form.is_valid())

    def test_tiket_form_valid(self):
        form = TiketForm(data={ 
            'service_date': (datetime.now() + timedelta(days=1)).date(),
            'service_time': datetime.now().time(),
            'specific_problems': 'masalah terakhir',
        })