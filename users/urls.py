from django.urls import path
from .views import BotLoginView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('telegram-login/', BotLoginView.as_view(),name='register'),
    path('refresh/', TokenRefreshView.as_view(), name='token update')
]


