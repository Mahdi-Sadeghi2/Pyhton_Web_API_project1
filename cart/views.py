# views.py

from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import ShoppingCart, CartItem
from store.models import Product


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        cart_info = ShoppingCart.objects.get_or_create(user=request.user)
        user_cart = cart_info[0]
        cart_created = cart_info[1]

        cart_item_info = CartItem.objects.get_or_create(
            shopping_cart=user_cart, product=product)
        cart_item = cart_item_info[0]
        item_created = cart_item_info[1]

        # Increment quantity, whether newly created or not
        cart_item.quantity += 1
        cart_item.save()

        return redirect('cart_view')


from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import ShoppingCart, CartItem
from store.models import Product

class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        cart_info = ShoppingCart.objects.get_or_create(user=request.user)
        user_cart = cart_info[0]
        cart_created = cart_info[1]

        cart_item_info = CartItem.objects.get_or_create(
            shopping_cart=user_cart, product=product)
        cart_item = cart_item_info[0]
        item_created = cart_item_info[1]

        # Increment quantity, whether newly created or not
        cart_item.quantity += 1
        cart_item.save()

        return redirect('cart_view')

class CartView(View):
    def get(self, request):
        cart_info = ShoppingCart.objects.get_or_create(user=request.user)
        user_cart = cart_info[0]
        cart_created = cart_info[1]

        cart_items = CartItem.objects.filter(shopping_cart=user_cart)
        total_quantity = sum(item.quantity for item in cart_items)

        # Calculate total price in the view
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        return render(request, 'cart/cart_view.html', {'cart_items': cart_items, 'total_quantity': total_quantity, 'total_price': total_price})
