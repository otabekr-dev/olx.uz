from django.urls import path
from .views import FavoriteView, FavoriteDeleteView, OrderView, OrderDetailView, ReviewListCreateView

urlpatterns = [
    path('favorites/', FavoriteView.as_view()),
    path('favorites/<int:pk>/', FavoriteDeleteView.as_view()),
    path('orders/', OrderView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
    path('reviews/', ReviewListCreateView.as_view())
]
