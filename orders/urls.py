from django.urls import path
from .views import FavoriteView, FavoriteDeleteView, OrderView, OrderDetailView

urlpatterns = [
    path('favorites/', FavoriteView.as_view()),
    path('favorites/<int:pk>/', FavoriteDeleteView.as_view()),
    path('orders/', OrderView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
]
