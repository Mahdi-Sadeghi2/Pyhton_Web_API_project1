from django.shortcuts import (render, redirect)
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.contrib import messages
from .models import Cart
import logging

logger = logging.getLogger(__name__)
def cart_detail(request):
    try:
        # Try to get or create a cart for the current user
        cart, _ = Cart.objects.get_or_create_cart(request)
    except Exception as e:
        messages.error(request, f"Error retrieving the cart: {str(e)}")
        return HttpResponseBadRequest("Error retrieving the cart")

    # Prepare context for rendering the cart details
    context = {
        'cart': cart,
    }

    return render(request, 'cart/cart_view.html', context)


def add_to_cart(request, product_id):
    try:
        # Try to get or create a cart for the current user
        cart, _ = Cart.objects.get_or_create_cart(request)

        # Validate product_id and quantity
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        # Add item to the cart
        item_data = {'product_id': product_id, 'quantity': quantity}
        cart.add_item(item_data)
        
        messages.success(request, "Item added to the cart successfully.")

    except Exception as e:
        logger.error(f"Error adding item to the cart: {str(e)}")
        messages.error(request, f"Error adding item to the cart: {str(e)}")

    return redirect(reverse('cart:cart_detail'))


def remove_from_cart(request, product_id):
    try:
        # Try to get or create a cart for the current user
        cart, _ = Cart.objects.get_or_create_cart(request)

        # Validate product_id
        if not cart.remove_item(product_id):
            messages.error(request, "Item not found in the cart.")
        else:
            messages.success(
                request, "Item removed from the cart successfully.")

    except Exception as e:
        logger.error(f"Error removing item from the cart: {str(e)}")
        messages.error(request, f"Error removing item from the cart: {str(e)}")

    return redirect(reverse('cart:cart_detail'))


def clear_cart(request):
    try:
        # Try to get or create a cart for the current user
        cart, _ = Cart.objects.get_or_create_cart(request)

        # Clear the cart
        cart.clear_cart()
        messages.success(request, "Cart cleared successfully.")
    except Exception as e:
        logger.error(f"Error clearing the cart: {str(e)}")
        messages.error(request, f"Error clearing the cart: {str(e)}")

    return redirect(reverse('cart:cart_detail'))
