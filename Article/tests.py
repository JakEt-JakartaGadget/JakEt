from django.test import TestCase
from .models import Artikel
from django.contrib.auth.models import User
from django.utils import timezone

class ArtikelModelTest(TestCase):
    
    def setUp(self):
        # Set up a user for the tests
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Set up an article instance
        self.artikel = Artikel.objects.create(
            title='Test Article',
            content='This is a test article content.',
            source='Test Source',
        )

    def test_artikel_creation(self):
        # Verify the article is created successfully
        self.assertEqual(self.artikel.title, 'Test Article')
        self.assertEqual(self.artikel.content, 'This is a test article content.')
        self.assertEqual(self.artikel.source, 'Test Source')
        self.assertIsNotNone(self.artikel.published_date)  # Ensure published_date is set

    def test_artikel_string_representation(self):
        # Check the string representation of the article
        self.assertEqual(str(self.artikel), 'Test Article')

    def test_artikel_image_field(self):
        # Test the image field (should be None if not provided)
        self.assertIsNone(self.artikel.image)  # Check if the image field is None

    def test_artikel_title_max_length(self):
        # Test that title max_length is enforced
        max_length = self.artikel._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_artikel_content_field(self):
        # Test the content field is not empty
        self.artikel.content = ''
        with self.assertRaises(ValueError):
            self.artikel.full_clean()  # Should raise an error because content is required

    def test_artikel_source_field(self):
        # Test that the source field can be blank
        self.artikel.source = ''
        self.artikel.save()  # Should not raise an error

    def test_artikel_published_date_auto_now_add(self):
        # Ensure published_date is set on creation
        new_artikel = Artikel.objects.create(
            title='New Article',
            content='Content of new article',
            source='New Source'
        )
        self.assertIsNotNone(new_artikel.published_date)

    def test_artikel_update(self):
        # Test that we can update an article's attributes
        self.artikel.title = 'Updated Title'
        self.artikel.save()
        self.assertEqual(self.artikel.title, 'Updated Title')

    def test_artikel_delete(self):
        # Test that we can delete an article
        artikel_id = self.artikel.id
        self.artikel.delete()
        with self.assertRaises(Artikel.DoesNotExist):
            Artikel.objects.get(id=artikel_id)

    def test_artikel_creation_with_image(self):
        # Test creating an article with an image
        self.artikel.image = 'dataset/article_image/iphone16.jpg'  # Simulate an image upload
        self.artikel.save()
        self.assertEqual(self.artikel.image, 'dataset/article_image/iphone16.jpg')
