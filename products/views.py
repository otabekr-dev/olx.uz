from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer
)
from .permissions import IsSellerOwnerOrReadOnly

class ProductListView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductListSerializer

    def get(self, request: Request):
        queryset = Product.objects.filter(status=Product.Status.ACTIVE).order_by('-created_at')

        search_query = request.GET.get('search')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductListSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)     

class ProductView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductListSerializer

    def get(self, request: Request) -> Response:
        products = Product.objects.filter(status=Product.Status.ACTIVE)
        serializer = ProductListSerializer(products, many=True)

        return Response(serializer.data)
    
    def post(self, request: Request) -> Response:
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(seller=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ProductDetailView(APIView):
    permission_classes = [IsSellerOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductDetailSerializer

    def get_object(self, pk: int):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request: Request, pk:int) -> Response:
        product = self.get_object(pk)

        if not product:
            return Response('Product mavjud emas', status=status.HTTP_404_NOT_FOUND)

        product.view_count += 1
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    def patch(self, request: Request, pk:int) -> Response:
        product = self.get_object(pk)

        if not product:
            return Response('Product mavjud emas', status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, product)
        serializer = ProductUpdateSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request: Request, pk:int) -> Response:
        product = self.get_object(pk)

        if not product:
            return Response('Product mavjud emas', status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, product)
        product.delete()
        return Response('Deleted', status=status.HTTP_204_NO_CONTENT)
    
class ProductPublishView(APIView):
    permission_classes = [IsSellerOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductDetailSerializer    

    def post(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({'detail': 'Product mavjud emas'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, product)
        product.status = Product.Status.ACTIVE
        product.save(update_fields=['status'])

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class ProductArchiveView(APIView):
    permission_classes = [IsSellerOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductDetailSerializer

    def post(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({'detail': 'Product mavjud emas'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, product)
        product.status = Product.Status.ARCHIVED
        product.save(update_fields=['status'])

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class ProductSoldView(APIView):
    permission_classes = [IsSellerOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductDetailSerializer
    
    def post(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({'detail': 'Product mavjud emas'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, product)
        product.status = Product.Status.SOLD
        product.seller.sellerprofile.total_sales += 1
        product.seller.sellerprofile.save(update_fields=['total_sales'])
        product.save(update_fields=['status'])

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)