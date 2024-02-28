import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Payment
from cart.models import Cart

logger = logging.getLogger(__name__)

def simulate_successful_payment(request, cart_id, amount):
    try:
        # Simulate a successful payment
        Payment.objects.create(amount=amount, status='success')
        Cart.objects.filter(id=cart_id).update(payment_status='success')
        messages.success(request, 'Payment successful!')
        return redirect(reverse('payment_result', args=[cart_id]))
    except Exception as e:
        logger.error(f"Error simulating successful payment: {str(e)}")
        messages.error(request, 'An error occurred during the payment process.')
        return redirect(reverse('payment_result', args=[cart_id]))

def simulate_unsuccessful_payment(request, cart_id, amount):
    try:
        # Simulate an unsuccessful payment
        Payment.objects.create(amount=amount, status='failure')
        Cart.objects.filter(id=cart_id).update(payment_status='failure')
        messages.error(request, 'Payment unsuccessful.')
        return redirect(reverse('payment_result', args=[cart_id]))
    except Exception as e:
        logger.error(f"Error simulating unsuccessful payment: {str(e)}")
        messages.error(request, 'An error occurred during the payment process.')
        return redirect(reverse('payment_result', args=[cart_id]))

def payment_result(request, cart_id):
    try:
        # Retrieve the payment status for the specified cart
        payment_status = Cart.objects.get(id=cart_id).payment_status
        return render(request, 'payment/payment_result.html', {'payment_status': payment_status})
    except Exception as e:
        logger.error(f"Error retrieving payment result: {str(e)}")
        messages.error(request, 'An error occurred while retrieving payment result.')
        return redirect(reverse('home'))  # Redirect to home or another appropriate page
