from django.test import TestCase
from store.models import (User, Product, Category, Price)
from .models import Cart, CartItem
from django.urls import reverse


class CartModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(
            username='testuser', password='testpassword')

        # Create a category
        self.category = Category.objects.create(name='Test Category')

        # Create a product with the created category
        self.product = Product.objects.create(
            name='Test Product', category=self.category, description='Test Description')

    def test_cart_creation(self):
        # Test creating a cart for a user
        cart = Cart.objects.create(customer=self.user)
        self.assertEqual(cart.status, 'active')
        self.assertEqual(cart.customer, self.user)
        self.assertEqual(cart.cart_items.count(), 0)

    def test_add_item_to_cart(self):
        # Test adding an item to the cart
        cart = Cart.objects.create(customer=self.user)
        item_data = {'product_id': self.product.id, 'quantity': 2}
        cart.add_item(item_data)
        self.assertEqual(cart.cart_items.count(), 1)
        self.assertEqual(cart.cart_items.first().quantity, 2)

    def test_remove_item_from_cart(self):
        # Test removing an item from the cart
        cart = Cart.objects.create(customer=self.user)
        item_data = {'product_id': self.product.id, 'quantity': 2}
        cart.add_item(item_data)
        cart.remove_item(self.product.id)
        self.assertEqual(cart.cart_items.count(), 0)

    def test_clear_cart(self):
        # Test clearing the cart
        cart = Cart.objects.create(customer=self.user)
        item_data = {'product_id': self.product.id, 'quantity': 2}
        cart.add_item(item_data)
        cart.clear_cart()
        self.assertEqual(cart.cart_items.count(), 0)

    def test_archive_cart(self):
        # Test archiving the cart
        cart = Cart.objects.create(customer=self.user)
        cart.archive_cart()
        self.assertEqual(cart.status, 'archived')


class CartItemModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(
            username='testuser', password='testpassword')

        # Create a test product
        self.product = Product.objects.create(
            name='Test Product', category=None, description='Test Description')

        # Create a test cart
        self.cart = Cart.objects.create(customer=self.user)

    def test_cart_item_creation(self):
        # Test creating a cart item
        cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2)
        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)


# This is view test

class CartViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create a test price
        self.price = Price.objects.create(amount=10.52, currency='USD')

        # Create a test product with the created price
        self.product = Product.objects.create(
            name='Test Product', price_item=self.price)

        # Create a cart for the user
        self.cart = Cart.objects.create(customer=self.user)

    def test_add_to_cart_view(self):
        response = self.client.post(reverse('cart:add_to_cart', args=[
                                    self.product.id]), {'quantity': 2})
        # Check if the redirect status is correct
        self.assertEqual(response.status_code, 302)

        # Refresh the cart to get the latest data from the database
        self.cart.refresh_from_db()

        # Print statements for debugging
        print("Response content:", response.content)
        print("Cart items:", self.cart.cart_items.all())

        # Check if the item is added to the cart
        self.assertTrue(self.cart.cart_items.filter(
            product=self.product, quantity=2).exists())

    def test_cart_detail_view(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

        # Print statements for debugging
        print("Response content:", response.content)

        # Check if the cart is present in the context
        self.assertIn('cart', response.context)
        self.assertIsInstance(response.context['cart'], Cart)

        # Check if the correct product and quantity are in the response content
        self.assertIn(str(self.product), str(response.content))
        self.assertIn('2', str(response.content))

    def test_remove_from_cart_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Simulate removing a product from the cart
        response = self.client.post(
            reverse('cart:remove_from_cart', args=[self.product.id]))
        # Expecting a redirect after removing from the cart
        self.assertEqual(response.status_code, 302)

        # Retrieve the cart and check if the item is removed
        cart = Cart.objects.get(customer=self.user)
        self.assertFalse(cart.cart_items.filter(
            product_id=self.product.id).exists())

    def test_clear_cart_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Simulate clearing the cart
        response = self.client.post(reverse('cart:clear_cart'))
        # Expecting a redirect after clearing the cart
        self.assertEqual(response.status_code, 302)

        # Retrieve the cart and check if it is cleared
        cart = Cart.objects.get(customer=self.user)
        self.assertEqual(cart.cart_items.count(), 0)
