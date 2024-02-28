# financial/urls.py
from django.urls import path
from .views import (simulate_successful_payment,
                    simulate_unsuccessful_payment, payment_result)


app_name = 'financial'
urlpatterns = [
    path('successful_payment/<int:payment_id>/',
         simulate_successful_payment, name='successful_payment'),
    path('unsuccessful_payment/<int:payment_id>/',
         simulate_unsuccessful_payment, name='unsuccessful_payment'),
    path('payment_result/<int:payment_id>/',
         payment_result, name='payment_result'),
]
