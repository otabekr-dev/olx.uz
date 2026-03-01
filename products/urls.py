from django.urls import path
from .views import (
    ProductListView,
    ProductView,
    ProductDetailView,
    ProductPublishView,
    ProductArchiveView,
    ProductSoldView
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Action endpoints
    path('products/<int:pk>/publish/', ProductPublishView.as_view(), name='product-publish'),
    path('products/<int:pk>/archive/', ProductArchiveView.as_view(), name='product-archive'),
    path('products/<int:pk>/sold/', ProductSoldView.as_view(), name='product-sold'),
]