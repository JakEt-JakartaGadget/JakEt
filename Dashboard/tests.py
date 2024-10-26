from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Homepage.models import Phone
import uuid

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

