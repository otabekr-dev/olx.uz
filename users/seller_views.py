from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializer import SellerProfileSerializer
from .models import SellerProfile
from .permissions import IsSeller

class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request) -> Response:
        user = request.user
        if SellerProfile.objects.filter(user=user).exists():
            return Response(
                {"detail": "Seller profili allaqachon mavjud."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SellerProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request: Request)-> Response:
        try:
            profile = SellerProfile.objects.get(user=request.user)
        except SellerProfile.DoesNotExist:
            return Response(
                {"detail": "Seller profili topilmadi."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SellerProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    