# financial/urls.py
from django.urls import path
from .views import PaymentListView, PaymentDetailView, simulate_successful_payment, simulate_unsuccessful_payment, payment_result


app_name = 'financial'
urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('simulate_successful_payment/<int:payment_id>/', simulate_successful_payment, name='simulate_successful_payment'),
    path('simulate_unsuccessful_payment/<int:payment_id>/', simulate_unsuccessful_payment, name='simulate_unsuccessful_payment'),
    path('payment_result/<int:payment_id>/', payment_result, name='payment_result'),
]
