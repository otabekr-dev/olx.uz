from django.urls import path
from .views import RegisterView, BotLoginView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('bot-login/', BotLoginView.as_view(),name='register'),
    path('refresh/', TokenRefreshView.as_view(), name='token update')
]
