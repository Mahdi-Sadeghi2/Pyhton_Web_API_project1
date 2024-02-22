# cart/urls.py
from django.urls import path
from .views import AddToCartView, CartView

app_name= 'cart'
urlpatterns = [
    path('add_to_cart/<int:product_id>/',
         AddToCartView.as_view(), name='add_to_cart'),
    path('cart_view/', CartView.as_view(), name='cart_view'),
]
