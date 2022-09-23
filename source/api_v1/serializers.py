from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from webapp.models import Product, Order


class ProductSerializer(serializers.Serializer):
    category_choices = [('other', 'Other'), ('dairy', 'Dairy'), ('soft_drinks', 'Soft Drinks'),
                        ('groceries', 'Groceries')]
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=2000, required=True)
    category = serializers.ChoiceField(choices=category_choices, default='1')
    remainder = serializers.IntegerField(max_value=None, min_value=0)
    price = serializers.DecimalField(max_digits=7, decimal_places=2)

    # def validate(self, attrs):
    #     return super().validate(attrs)
    #
    # def validate_title(self, value):
    #     return value
    #
    # def create(self, validated_data):
    #     return Article.objects.create(**validated_data)
    #
    # def update(self, instance: Article, validated_data):
    #     for field, value in validated_data.items():
    #         setattr(instance, field, value)
    #     instance.save()
    #     return instance


class ProductModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["name", "id"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "id")


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    phone = serializers.CharField(max_length=100, required=True)
    address = serializers.CharField(max_length=100, required=True)
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)


class OrderModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["id", "created_at", ]