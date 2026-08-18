from rest_framework import serializers
from decimal import Decimal
from .models import Box, Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= "__all__"


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    recommended_box = BoxSerializer(read_only=True)
    class Meta:
        model = Order
        fields ="__all__"


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),source="product",)
    quantity = serializers.IntegerField(required=False,default=1,min_value=1,)


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemInputSerializer(many=True)
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError(
                "At least one item is required."
            )
        return value

    def create(self, validated_data):
        items_data = validated_data["items"]
        order = Order.objects.create()
        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                )
                for item in items_data
            ]
        )
        return order


class AdHocRecommendRequestSerializer(serializers.Serializer):
    items = OrderItemInputSerializer(many=True)
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required.")
        return value