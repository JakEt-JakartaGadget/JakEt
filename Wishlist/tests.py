from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Homepage.models import Phone
from .models import Favorite
import uuid

class WishlistTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.phone = Phone.objects.create(
            brand="Apple", model="iPhone 13", storage="128GB", ram="4GB",
            screen_size_inches=6.1, camera_mp="12MP", battery_capacity_mAh=3240,
            price_usd=799, price_inr=59000, rating=4, image_url="https://example.com/image.jpg"
        )
        self.favorite = Favorite.objects.create(user=self.user, phone=self.phone)

    def test_favorite_list_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('Wishlist:favorite_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist.html')
        self.assertIn('favorites', response.context)
        self.assertEqual(response.context['favorites'].count(), 1)
        self.assertEqual(response.context['favorites'][0].phone.model, "iPhone 13")

    def test_remove_favorite_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('Wishlist:remove_favorite', args=[self.phone.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Wishlist:favorite_list'))
        self.assertFalse(Favorite.objects.filter(user=self.user, phone=self.phone).exists())
    
    def test_remove_favorite_nonexistent_phone(self):
        self.client.login(username='testuser', password='password')
        non_existent_phone_id = uuid.uuid4()
        response = self.client.post(reverse('Wishlist:remove_favorite', args=[non_existent_phone_id]))
        self.assertEqual(response.status_code, 404)  
