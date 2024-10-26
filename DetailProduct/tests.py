from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Homepage.models import Phone
from DetailProduct.models import Review
from Wishlist.models import Favorite


class DetailProductTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)
        self.phone = Phone.objects.create(
            brand="Apple", model="iPhone 13", storage="128GB", ram="4GB",
            screen_size_inches=6.1, camera_mp="12MP", battery_capacity_mAh=3240,
            price_usd=799, price_inr=59000, rating=4, image_url="https://example.com/image.jpg"
        )
        self.review = Review.objects.create(
            user=self.user, product=self.phone, content="Great phone!", rating=5
        )
        self.favorite = Favorite.objects.create(user=self.user, phone=self.phone)

    def test_product_detail_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('DetailProduct:detail_page', args=[self.phone.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'].model, "iPhone 13")

    def test_toggle_favorite_add(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('Homepage:toggle_favorite', args=[self.phone.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'is_favorite': False})  # Karena sudah difavoritkan, jadi akan dihapus

    def test_toggle_favorite_remove(self):
        self.client.login(username='testuser', password='password')
        self.favorite.delete()  # Menghapus favorite awal
        response = self.client.post(reverse('Homepage:toggle_favorite', args=[self.phone.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'is_favorite': True})

    def test_review_page_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('DetailProduct:review_page', args=[self.phone.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_page.html')
        self.assertIn('product', response.context)
        self.assertIn('reviews', response.context)
        self.assertEqual(response.context['product'].model, "iPhone 13")

    def test_edit_review_view_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('DetailProduct:edit_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_review.html')
        self.assertIn('review', response.context)
        self.assertEqual(response.context['review'].content, "Great phone!")

    def test_edit_review_view_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('DetailProduct:edit_review', args=[self.review.id]), {
            'rating': 3,
            'content': "Updated review content."
        })
        self.assertEqual(response.status_code, 302)  # Redirect setelah update
        self.review.refresh_from_db()
        self.assertEqual(self.review.content, "Updated review content.")
        self.assertEqual(self.review.rating, 3)

    def test_delete_review_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('DetailProduct:delete_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('DetailProduct:review_page', args=[self.phone.id]))
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_review_access_denied_for_other_users(self):
        another_user = User.objects.create_user(username='anotheruser', password='password')
        self.client.login(username='anotheruser', password='password')
        response = self.client.get(reverse('DetailProduct:edit_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 302)  
        response = self.client.post(reverse('DetailProduct:delete_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())  

