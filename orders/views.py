from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

from products.models import Product
from .models import Favorite
from .serializers import FavoriteCreateSerializer, FavoriteListSerializer


class FavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request: Request) -> Response:
        favorites = Favorite.objects.filter(user=request.user)

        serializer = FavoriteListSerializer(favorites, many=True)
        return Response(serializer.data)
    
    def post(self, request: Request) -> Response:
        serializer = FavoriteCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            product_id = serializer.validated_data['product_id']

            product = Product.objects.filter(id=product_id).first()

            if not product:
                return Response('Maxsulot mavjud emas', status=status.HTTP_404_NOT_FOUND)
            
            if Favorite.objects.filter(user=request.user, product=product).exists():
                return Response('Allaqchon favorite larga qushilgan', status=status.HTTP_400_BAD_REQUEST)
            
            favorite = Favorite.objects.create(
                user=request.user,
                product=product
            )

            return Response('Favorites ga qushildi', status=status.HTTP_200_OK)

class FavoriteDeleteView(APIView):
    permission_classes = [IsAuthenticated]        
    authentication_classes = [JWTAuthentication]

    def delete(self, request: Request, pk:int) -> Response:
        fav = Favorite.objects.filter(user=request.user, pk=pk)

        if not fav:
            return Response('Product mavjud emas', status=status.HTTP_404_NOT_FOUND)
        
        fav.delete()

        return Response(
            "Favoritesdan olib tashlandi",
            status=status.HTTP_204_NO_CONTENT
        )
    
