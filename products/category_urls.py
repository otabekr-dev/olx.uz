from django.urls import path
from .category_views import CategoryView, CategoryDetailView, CategoryProductView, CategorySlugView

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<slug:slug>/', CategorySlugView.as_view()),
    path('categories/<slug:slug>/products/', CategoryProductView.as_view()),    
]