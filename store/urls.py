from django.urls import path
from .views import CategoryListView, CategoryDetailView, ProductListView, ProductDetailView
from django.contrib.auth import views as auth_views


app_name= 'store'
urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    # path('products/<int:pk>/add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    # path('signup/', SignUpView.as_view(), name='signup'),
    # path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    
]
