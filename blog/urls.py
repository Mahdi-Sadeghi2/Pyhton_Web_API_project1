from django.urls import path
from .views import CategoryListView, CategoryDetailView, ContentListView, ContentDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('contents/', ContentListView.as_view(), name='content_list'),
    path('contents/<int:pk>/', ContentDetailView.as_view(), name='content_detail'),
]