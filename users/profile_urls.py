from django.urls import path
from .views import ProfileView
from .seller_views import SellerProfileView, SellerDetailView, SellerProducts
from .views import Change2SellerView

urlpatterns = [
    path('me/', ProfileView.as_view()),
    path('seller/', SellerProfileView.as_view()),
    path('me/upgrade-to-seller/', Change2SellerView.as_view()),
    path('sellers/<int:pk>/', SellerDetailView.as_view()),
    path('sellers/<int:pk>/products/', SellerProducts.as_view()),
]