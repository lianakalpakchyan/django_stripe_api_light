from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

import stripe
from django.views import View
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .enums import CurrencyEnum
from .models import Item, Order, OrderItem, Discount, Tax
from .serializers import OrderSerializer, OrderItemSerializer, DiscountSerializer, TaxSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemListView(View):
    def get(self, request):
        currency = request.GET.get('currency', CurrencyEnum.USD.value)
        items = Item.objects.filter(currency=currency)
        return render(
            request,
            'items/items.html',
            {'items': items, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
        )


class ItemDetailView(View):
    def get(self, request, item_id):
        item = Item.objects.filter(id=item_id).first()
        return render(
            request,
            'items/item.html',
            {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
        )


class OrderAPIDetailView(generics.RetrieveUpdateDestroyAPIView, generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
        order_code = self.request.headers.get("X-Order-Code")

        if not order_code:
            raise NotFound("Order code header is missing.")

        try:
            return Order.objects.get(order_code=order_code)
        except Order.DoesNotExist:
            raise NotFound("Order not found.")

    def post(self, request, *args, **kwargs):
        order_code = self.request.headers.get("X-Order-Code")
        item_id = request.data.get("item_id")

        order, created = Order.objects.get_or_create(order_code=order_code)
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise NotFound("Item not found.")

        # This part makes sure all the items in the order have the same currency
        # If there is already at least one item in the order the new one should have the same currency as that one
        if not created and (orderitem := order.orderitems.all().first()):
            currency = orderitem.item.currency
            if item.currency != currency:
                return JsonResponse(
                    {'error': f'Only items with currency: {currency} can be added to the current order'},
                    status=400)

        orderitem, created = OrderItem.objects.get_or_create(order=order, item=item)
        orderitem.quantity = 1 if created else orderitem.quantity + 1
        orderitem.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderItemAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class DiscountList(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class TaxList(generics.ListCreateAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


class SuccessView(View):
    def get(self, request):
        return render(
            request,
            'items/success.html',
            {"hide_order": True}
        )


@api_view(["POST"])
def buy(request):
    order_code = request.headers.get("X-Order-Code")
    discounts = []

    if order_code:
        try:
            order = Order.objects.get(order_code=order_code)
        except Order.DoesNotExist:
            raise NotFound("Order not found.")

        if not order.orderitems.all():
            return Response({"error": "Order is empty."}, status=400)

        tax_rate = stripe.TaxRate.create(
            display_name=order.tax.display_name,
            inclusive=order.tax.inclusive,
            percentage=order.tax.percentage
        ) if order.tax else None

        line_items = [
            {
                "price_data": {
                    "currency": item.item.currency,
                    "product_data": {"name": item.item.name},
                    "unit_amount": int(item.item.price * 100),
                },
                "quantity": item.quantity,
                "tax_rates": [tax_rate.id] if tax_rate else [],
            }
            for item in order.orderitems.all()
        ]
        if order.discount and order.discount.percent_off:
            discounts.append({'coupon': stripe.Coupon.create(percent_off=order.discount.percent_off)})

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                discounts=discounts,
                success_url=f"{settings.SUCCESS_URL}/success",
            )
            return Response(checkout_session)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
    else:
        return Response({"error": "Order code header is missing."}, status=404)
