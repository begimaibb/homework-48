from itertools import product

from django.db.models import Count
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404


from api_v1.serializers import ProductModelsSerializer, OrderModelsSerializer
from webapp.models import Product, Order


class ProductView(APIView):
    serializer_class = ProductModelsSerializer

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        products_data = self.serializer_class(products, many=True).data
        return Response(products_data)

    def post(self, request, *args, **kwargs):
        print(request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def put(self, request, *args, pk, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelsSerializer
    # permission_classes = [IsAuthenticated, DjangoModelPermissions]

    # @action(methods=["GET"], detail=True, url_path="comments-count")
    # def get_comments_count(self, request, *args, **kwargs):
    #     print(kwargs)
    #     return Response({"count": self.get_object().comments.count()})

    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         return [AllowAny]
    #     return super().get_permissions()


class OrderView(APIView):
    serializer_class = OrderModelsSerializer

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        orders_data = self.serializer_class(orders, many=True).data
        return Response(orders_data)

    def post(self, request, *args, **kwargs):
        print(request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelsSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response({'status': 'ok'})
