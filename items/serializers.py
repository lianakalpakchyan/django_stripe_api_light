from rest_framework import serializers
from rest_framework.fields import IntegerField

from items.models import OrderItem, Order, Item, Discount, Tax


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "price", "currency"]


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ["id", "percent_off"]


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ["id", "display_name", "inclusive", "percentage"]


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemListSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "item", "quantity", "sub_total"]

    def get_sub_total(self, order_item):
        total = order_item.item.price * order_item.quantity
        return total
    
    def validate(self, data):
        quantity = data.get("quantity")

        if quantity is not None and quantity <= 0:
            raise serializers.ValidationError({
                "error": "Quantity must be greater than 0"
            })
        return data


class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, read_only=True)
    discount = DiscountSerializer(read_only=True)
    tax = TaxSerializer(read_only=True)
    tax_id = IntegerField(write_only=True)
    discount_id = IntegerField(write_only=True)
    order_total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["order_code", "orderitems", "order_total", "discount", "tax", "tax_id", "discount_id"]

    def get_order_total(self, order):
        items = order.orderitems.all()
        total = sum([item.quantity * item.item.price for item in items])
        return total

    def validate(self, data):
        tax_id = data.get("tax_id")

        if tax_id and not Tax.objects.filter(id=tax_id).exists():
            raise serializers.ValidationError({
                "error": "Tax with this tax_id does not exist."
            })

        discount_id = data.get("discount_id")

        if discount_id and not Discount.objects.filter(id=discount_id).exists():
            raise serializers.ValidationError({
                "error": "Discount with this discount_id does not exist."
            })

        return data
