from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from .models import Category
from .category_serializers import CategorySerializer

class CategoryView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

    def get(self, request: Request) -> Response:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    

    def post(self, request: Request) -> Response:
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CategoryDetailView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

    def get_object(self, pk):
        try:
             return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request: Request, pk) -> Response:
        category = self.get_object(pk)
        if not category:
            return Response({'detail': 'Category mavjud emas'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request:Request, pk) -> Response:
        category = self.get_object(pk)
        if not category:
            return Response({'detail': 'Category mavjud emas'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request:Request, pk) -> Response:
        category = self.get_object(pk)
        if not category:
            return Response({'detail': 'Category mavjud emas'}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
