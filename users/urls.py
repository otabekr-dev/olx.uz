from django.urls import path
from .views import BotLoginView, LogOutView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('telegram-login/', BotLoginView.as_view(),name='register'),
    path('logout/', LogOutView.as_view(),name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token update')
]


