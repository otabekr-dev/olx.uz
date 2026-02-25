from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import RegisterSerializer

User = get_user_model()

BOT_LINK = "https://t.me/olxauthbot"

class RegisterView(APIView):

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        
        
        if serializer.is_valid(raise_exception=True):

            data = serializer.validated_data

            user = User.objects.create_user(
                username=data["username"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                password=data["password"]
            )

            if "avatar" in data:
                user.avatar = data["avatar"]
                user.save()

            return Response(
                {
                    "message": "User yaratildi",
                    "token uchun bot": BOT_LINK
                },
                status=status.HTTP_201_CREATED
            )

class BotLoginView(APIView):
    """
    Telegram bot orqali login qilish.
    Foydalanuvchi:
    - username
    - password
    - telegram_id
    yuboradi.
    Agar username/password to'g'ri bo'lsa, access va refresh token qaytariladi.
    Telegram ID foydalanuvchiga bog'lanadi.
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        telegram_id = request.data.get("telegram_id")

        if not username or not password or not telegram_id:
            return Response(
                {"detail": "Username, password va telegram_id majburiy"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "Username topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not check_password(password, user.password):
            return Response(
                {"detail": "Password noto'g'ri"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user.telegram_id = telegram_id
        user.save()


        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            "access": access,
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
        