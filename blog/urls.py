from django.urls import path
from .views import CategoryListView, CategoryDetailView, ContentListView, ContentDetailView, CustomLoginView, SignUpView
from django.contrib.auth import views as auth_views


app_name= 'blog'
urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('contents/', ContentListView.as_view(), name='content_list'),
    path('contents/<int:pk>/', ContentDetailView.as_view(), name='content_detail'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
]