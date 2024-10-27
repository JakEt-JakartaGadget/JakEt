from django.test import TestCase
from .models import Artikel
from django.contrib.auth.models import User
from django.urls import reverse

class ArtikelModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.artikel = Artikel.objects.create(
            title='Test Article',
            content='This is a test article content.',
            source='Test Source',
        )

    def test_artikel_creation(self):
        self.assertEqual(self.artikel.title, 'Test Article')
        self.assertEqual(self.artikel.content, 'This is a test article content.')
        self.assertEqual(self.artikel.source, 'Test Source')
        self.assertIsNotNone(self.artikel.published_date)

    def test_artikel_string_representation(self):
        self.assertEqual(str(self.artikel), 'Test Article')

    def test_artikel_title_max_length(self):
        max_length = self.artikel._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_artikel_source_field(self):
        self.artikel.source = ''
        self.artikel.save()

    def test_artikel_published_date_auto_now_add(self):
        new_artikel = Artikel.objects.create(
            title='New Article',
            content='Content of new article',
            source='New Source'
        )
        self.assertIsNotNone(new_artikel.published_date)

    def test_artikel_update(self):
        self.artikel.title = 'Updated Title'
        self.artikel.save()
        self.assertEqual(self.artikel.title, 'Updated Title')

    def test_artikel_delete(self):
        artikel_id = self.artikel.id
        self.artikel.delete()
        with self.assertRaises(Artikel.DoesNotExist):
            Artikel.objects.get(id=artikel_id)

    def test_artikel_creation_with_image(self):
        self.artikel.image = 'article_image/iphone16.jpg'
        self.artikel.save()
        self.assertEqual(self.artikel.image, 'article_image/iphone16.jpg')


class ArtikelViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass') 
        self.client.login(username='admin', password='adminpass')  
        self.artikel = Artikel.objects.create(
            title='Test Article',
            content='This is a test article content.',
            source='Test Source',
        )



