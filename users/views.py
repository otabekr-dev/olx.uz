import requests
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsCustomer

User = get_user_model()

class BotLoginView(APIView):
    
    def post(self, request: Request) -> Response:
        telegram_id = request.data.get("telegram_id")
        username = request.data.get("username")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        photo_url = request.data.get("photo_url")  

        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": username or f"tg_{telegram_id}",
                "first_name": first_name,
                "last_name": last_name,
                "role": User.Role.CUSTOMER,
            }
        )

        if photo_url:
            resp = requests.get(photo_url)
            if resp.status_code == 200:
                user.avatar.save(f"{telegram_id}.jpg", ContentFile(resp.content), save=True)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserProfileSerializer

    def get(self, request):

        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True  
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Change2SellerView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        if user.role == 'CUSTOMER':
            user.role = 'SELLER'
            user.save(update_fields=['role'])
            return Response(
                {"detail": "User seller ga o'zgartirildi"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "User allaqachon seller"},
            status=status.HTTP_400_BAD_REQUEST
        )

