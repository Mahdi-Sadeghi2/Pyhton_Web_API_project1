from django.urls import path
from .views import CategoryListView, CategoryDetailView, ContentListView, ContentDetailView, CustomLoginView, SignUpView,CustomLogoutView



app_name= 'blog'
urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('contents/', ContentListView.as_view(), name='content_list'),
    path('contents/<int:pk>/', ContentDetailView.as_view(), name='content_detail'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
]