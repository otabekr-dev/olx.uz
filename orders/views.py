from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

from products.models import Product
from .models import Favorite, Order, Review
from .serializers import (
    FavoriteCreateSerializer, FavoriteListSerializer,
    OrderCreateSerializer, OrderDetailSerializer,
    OrderUpdateSerializer, OrderListSerializer
)


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

            favorite.product.favorite_count += 1
            favorite.product.save()

            return Response('Favorites ga qushildi', status=status.HTTP_200_OK)

class FavoriteDeleteView(APIView):
    permission_classes = [IsAuthenticated]        
    authentication_classes = [JWTAuthentication]

    def delete(self, request: Request, pk:int) -> Response:
        favorite = Favorite.objects.filter(pk=pk, user=request.user).first()

        if not favorite:
            return Response(
                {"detail": "Favorite topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )

        product = favorite.product

        if product.favorite_count > 0:
            product.favorite_count -= 1
            product.save()

        favorite.delete()

        return Response('Deleted',status=status.HTTP_204_NO_CONTENT)
    

class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request: Request):

        role = request.query_params.get('role')

        if role == 'buyer':
            orders = Order.objects.filter(buyer=request.user)

        elif role == 'seller':
            orders = Order.objects.filter(seller=request.user)

        else:
            orders = Order.objects.filter(
                buyer=request.user
            ) | Order.objects.filter(
                seller=request.user
            )

        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)


    def post(self, request: Request):

        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product mavjud emas"},
                status=status.HTTP_404_NOT_FOUND
            )

        order = Order.objects.create(
            product=product,
            buyer=request.user,
            seller=product.seller,
            final_price=product.price,
            notes=serializer.validated_data.get('notes', '')
        )

        return Response(
            OrderDetailSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get_object(self, pk:int):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None


    def get(self, request: Request, pk: int):

        order = self.get_object(pk)

        if not order:
            return Response(
                {"detail": "Order mavjud emas"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user not in [order.buyer, order.seller]:
            return Response(
                {"detail": "Ruxsat yo'q"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)
    

    def patch(self, request: Request, pk: int):

        order = self.get_object(pk)

        if not order:
            return Response(
                {"detail": "Order mavjud emas"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderUpdateSerializer(order, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)

        status_value = serializer.validated_data.get('status')


        if request.user == order.seller:

            if order.status == Order.Status.PENDING and status_value == Order.Status.AGREED:
                serializer.save()

            elif status_value == Order.Status.CANCELLED:
                serializer.save()

            else:
                return Response(
                    {"detail": "Seller bu statusga o'zgartira olmaydi"},
                    status=status.HTTP_400_BAD_REQUEST
                )


        elif request.user == order.buyer:

            if order.status == Order.Status.AGREED and status_value == Order.Status.COMPLETED:

                serializer.save()

                product = order.product
                product.status = Product.Status.SOLD
                product.save(update_fields=['status'])

                seller_profile = order.seller.sellerprofile
                seller_profile.total_sales += 1
                seller_profile.save(update_fields=['total_sales'])

            elif status_value == Order.Status.CANCELLED:
                serializer.save()

            else:
                return Response(
                    {"detail": "Buyer bu statusga o'zgartira olmaydi"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {"detail": "Ruxsat yo'q"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(OrderDetailSerializer(order).data)