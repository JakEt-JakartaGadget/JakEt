from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Phone
from Wishlist.models import Favorite
import uuid

class HomepageTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.phone1 = Phone.objects.create(
            brand="Apple", model="iPhone 13", storage="128GB", ram="4GB",
            screen_size_inches=6.1, camera_mp="12MP", battery_capacity_mAh=3240,
            price_usd=799, price_inr=59000, rating=4, image_url="https://example.com/image.jpg"
        )
        self.phone2 = Phone.objects.create(
            brand="Samsung", model="Galaxy S21", storage="256GB", ram="8GB",
            screen_size_inches=6.2, camera_mp="64MP", battery_capacity_mAh=4000,
            price_usd=699, price_inr=52000, rating=5, image_url="https://example.com/image2.jpg"
        )
        self.favorite = Favorite.objects.create(user=self.user, phone=self.phone1)

    def test_home_section_view(self):
        response = self.client.get(reverse('Homepage:home_section'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('phones', response.context)
        self.assertIn('user_favorites', response.context)

    def test_list_products_view(self):
        response = self.client.get(reverse('Homepage:list_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_product.html')
        self.assertIn('phones', response.context)
        self.assertIn('brands', response.context)
        self.assertIn('storages', response.context)
        self.assertIn('rams', response.context)

    def test_list_products_filter(self):
        response = self.client.get(reverse('Homepage:list_product'), {'brand': 'Apple'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['phones']), 1)
        self.assertEqual(response.context['phones'][0].brand, 'Apple')

    def test_list_products_sorting(self):
        response = self.client.get(reverse('Homepage:list_product'), {'sort_price': 'low_to_high'})
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(response.context['phones'][0].price_inr, response.context['phones'][1].price_inr)

    def test_toggle_favorite_add(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('Homepage:toggle_favorite', args=[self.phone2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(user=self.user, phone=self.phone2).exists())
        self.assertJSONEqual(response.content, {'is_favorite': True})

    def test_toggle_favorite_remove(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('Homepage:toggle_favorite', args=[self.phone1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favorite.objects.filter(user=self.user, phone=self.phone1).exists())
        self.assertJSONEqual(response.content, {'is_favorite': False})

    def test_search_results_view(self):
        response = self.client.get(reverse('Homepage:search_results'), {'q': 'Apple'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')
        self.assertIn('phones', response.context)
        self.assertEqual(len(response.context['phones']), 1)
        self.assertEqual(response.context['phones'][0].brand, 'Apple')

    def test_search_results_no_match(self):
        response = self.client.get(reverse('Homepage:search_results'), {'q': 'UnknownBrand'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, we can't find your product.")

    def test_search_suggestions_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('Homepage:search_suggestions'), {'q': 'iPhone'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['brand'], 'Apple')
        self.assertEqual(response.json()[0]['model'], 'iPhone 13')

    def test_phone_model_avg_rating(self):
        phone = Phone.objects.get(model="iPhone 13")
        phone.one_star = 1
        phone.two_star = 1
        phone.three_star = 1
        phone.four_star = 1
        phone.five_star = 1
        self.assertEqual(phone.avg_rating, 3.0)

    def test_phone_model_total_respondents(self):
        phone = Phone.objects.get(model="iPhone 13")
        phone.one_star = 1
        phone.two_star = 1
        phone.three_star = 1
        phone.four_star = 1
        phone.five_star = 1
        self.assertEqual(phone.total_respondents, 5)
