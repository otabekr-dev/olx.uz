from django.urls import path
from .views import FavoriteView, FavoriteDeleteView

urlpatterns = [
    path('favorites/', FavoriteView.as_view()),
    path('favorites/<int:pk>/', FavoriteDeleteView.as_view()),
]
