from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Payment
from cart.models import ShoppingCart


class PaymentListView(View):
    def get(self, request):
        payments = Payment.objects.all()
        return render(request, 'financial/payment_list.html', {'payments': payments})

class PaymentDetailView(View):
    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        return render(request, 'financial/payment_detail.html', {'payment': payment})

def simulate_successful_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    payment.payment_status = 'success'
    payment.save()
    return redirect('payment_result', payment_id=payment.id)

def simulate_unsuccessful_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    payment.payment_status = 'failure'
    payment.save()
    return redirect('payment_result', payment_id=payment.id)

def payment_result(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    return render(request, 'financial/payment_result.html', {'payment': payment})
