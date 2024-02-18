from django.urls import path

urlpatterns = [
    path('categories/', category_list, name='category_list'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),
    path('contents/', content_list, name='content_list'),
    path('contents/<int:content_id>/', content_detail, name='content_detail')
    
]