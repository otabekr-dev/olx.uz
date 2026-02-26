from django.urls import path
from .views import ProfileView
from .seller_views import SellerProfileView
from .views import Change2SellerView

urlpatterns = [
    path('profile/me/', ProfileView.as_view()),
    path('seller/', SellerProfileView.as_view()),
    path('upgrade-to-seller/<int:pk>/e', Change2SellerView.as_view()),
]