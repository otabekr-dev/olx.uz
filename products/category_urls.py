from django.urls import path
from .category_views import CategoryView, CategoryDetailView

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]