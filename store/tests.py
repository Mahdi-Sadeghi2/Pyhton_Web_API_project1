from django.test import TestCase
from django.contrib.auth.models import User
from .models import (Category, Price, Media, Product, UserComment)
from django.urls import reverse
from .views import (CategoryListView, ProductListView,
                    ProductDetailView, CategoryDetailView)

# Create your tests here.


class ModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='user123', password='123456Mc@')

        # Create test category
        self.category = Category.objects.create(name='Test Category')

        # Create test price
        self.price = Price.objects.create(amount=10.5, currency='USD')

        # Create test media
        self.media = Media.objects.create(media='puzzle.jpg')

    def test_category_creation(self):
        # Test category creation
        category = Category.objects.create(name='New Category')
        self.assertEqual(category.name, 'New Category')

    def test_price_creation(self):
        # Test price creation
        price = Price.objects.create(amount=20.5, currency='EUR')
        self.assertEqual(str(price), '20.5 EUR')

    def test_media_creation(self):
        # Test media creation
        media = Media.objects.create(media='default_video.mp4')
        self.assertEqual(media.media, 'default_video.mp4')

    def test_product_creation(self):
        # Test product creation
        product = Product.objects.create(
            name='Test Product',
            category=self.category,
            description='Test Description',
            media=self.media,
            price_item=self.price  # Use the already created price
        )
        self.assertEqual(product.name, 'Test Product')
        # Access price_item instead of price_items
        self.assertEqual(product.price_item.amount, 10.5)

    def test_user_comment_creation(self):
        # Test user comment creation
        user_comment = UserComment.objects.create(
            user=self.user,
            product=Product.objects.create(
                name='Test Product', category=self.category),
            comment_text='Test Comment',
            enabled=True,
            approved_by_admin=True
        )
        self.assertEqual(user_comment.comment_text, 'Test Comment')
        self.assertTrue(user_comment.enabled)
        self.assertTrue(user_comment.approved_by_admin)

# This is a test view


class StoreViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # Create test category
        self.category = Category.objects.create(name='Test Category')

        # Create test product
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            description='Test Description'
        )

    def test_category_list_view(self):
        # Test the category list view
        response = self.client.get(reverse('store:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/category_list.html')
        self.assertIsInstance(response.context['view'], CategoryListView)
        # Check if the category name is present in the response content
        self.assertContains(response, self.category.name)

    def test_category_detail_view(self):
        # Test the category detail view
        response = self.client.get(
            reverse('store:category_detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/category_detail.html')
        self.assertIsInstance(response.context['view'], CategoryDetailView)
        # Check if the product name is present in the response content
        self.assertContains(response, self.product.name)

    def test_product_list_view(self):
        # Test the product list view
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_list.html')
        self.assertIsInstance(response.context['view'], ProductListView)
        # Check if the product name is present in the response content
        self.assertContains(response, self.product.name)

    def test_login_view(self):
        # Test the login view
        response = self.client.get(reverse('store:login'))
        self.assertEqual(response.status_code, 200)
        # Case-insensitive check
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_signup_view(self):
        # Test the signup view
        response = self.client.get(reverse('store:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_product_detail_view_authenticated_user(self):
        # Test the product detail view with an authenticated user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('store:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_detail.html')
        self.assertIsInstance(response.context['view'], ProductDetailView)
        # Check if the comment form is present for authenticated users
        self.assertContains(response, 'Comment Form')

    def test_logout_view(self):
        # Test the logout view
        # Use post instead of get
        response = self.client.post(reverse('store:logout'))
        # Update the expected status code to 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logged_out.html')

    def test_home_view(self):
        # Test the home view
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_product_detail_view_authenticated_user(self):
        # Test the product detail view with an authenticated user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('store:product_detail', args=[self.product.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        # Check if the product name is present
        self.assertContains(response, self.product.name)

    def test_authenticated_user_comment_submission(self):
        # Test authenticated user comment submission
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('store:product_detail', args=[
                                    self.product.id]), {'comment_text': 'Test comment'})
        # Expecting a redirect after successful comment submission
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserComment.objects.count(), 1)
        comment = UserComment.objects.first()
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.comment_text, 'Test comment')
        self.assertFalse(comment.enabled)
        self.assertFalse(comment.approved_by_admin)
