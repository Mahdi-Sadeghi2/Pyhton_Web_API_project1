from django.test import TestCase
from django.contrib.auth.models import User
from .models import (ContentCategory, Content, Image, Video, UserComment)
from django.urls import reverse


class ModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # Create test category
        self.category = ContentCategory.objects.create(name='Test Category')

        # Create test image
        self.image = Image.objects.create(image='test_image.jpg')

        # Create test video
        self.video = Video.objects.create(video='test_video.mp4')

    def test_content_category_creation(self):
        category = ContentCategory.objects.create(name='New Category')
        self.assertEqual(category.name, 'New Category')

    def test_content_creation(self):
        content = Content.objects.create(
            title='Test Content',
            category=self.category,
            description='Test Description'
        )
        content.image_gallery.add(self.image)
        content.video_gallery.add(self.video)

        self.assertEqual(content.title, 'Test Content')
        self.assertEqual(content.category, self.category)
        self.assertEqual(content.description, 'Test Description')
        self.assertIn(self.image, content.image_gallery.all())
        self.assertIn(self.video, content.video_gallery.all())

    def test_image_creation(self):
        image = Image.objects.create(image='sound-toy1.jpg')
        # Extract the file name for comparison
        self.assertEqual(image.image.name, 'sound-toy1.jpg')

    def test_video_creation(self):
        video = Video.objects.create(video='defaul_video.mp4')
        # Extract the file name for comparison
        self.assertEqual(video.video.name, 'defaul_video.mp4')

    def test_user_comment_creation(self):
        user_comment = UserComment.objects.create(
            user=self.user,
            content=Content.objects.create(
                title='Test Content', category=self.category),
            comment_text='Test Comment',
            enabled=True,
            approved_by_admin=True
        )
        self.assertEqual(user_comment.comment_text, 'Test Comment')
        self.assertTrue(user_comment.enabled)
        self.assertTrue(user_comment.approved_by_admin)

# This is views test


class BlogViewsTest(TestCase):

    def setUp(self):
        self.category = ContentCategory.objects.create(name='Test Category')
        self.content = Content.objects.create(
            title='Test Content',
            category=self.category,
            description='Lorem ipsum dolor sit amet.'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_category_list_view(self):
        response = self.client.get(reverse('blog:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category_list.html')

    def test_category_detail_view(self):
        response = self.client.get(
            reverse('blog:category_detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category_detail.html')
        self.assertEqual(response.context['category'], self.category)

    def test_content_list_view(self):
        response = self.client.get(reverse('blog:content_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/content_list.html')

    def test_content_detail_view(self):
        response = self.client.get(
            reverse('blog:content_detail', args=[self.content.id]))
        expected_url = f'/blog/login/?next={
            reverse("blog:content_detail", args=[self.content.id])}'
        self.assertRedirects(response, expected_url)

    def test_login_view(self):
        response = self.client.get(reverse('blog:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_signup_view(self):
        response = self.client.get(reverse('blog:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_logout_view(self):
        # Use post instead of get
        response = self.client.post(reverse('blog:logout'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_comment_submission(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('blog:content_detail', args=[self.content.id]),
            {'comment_text': 'Test comment'}
        )
        # Expecting a redirect after successful comment submission
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserComment.objects.count(), 1)
        comment = UserComment.objects.first()
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.content, self.content)
        self.assertEqual(comment.comment_text, 'Test comment')
        self.assertFalse(comment.enabled)
        self.assertFalse(comment.approved_by_admin)
