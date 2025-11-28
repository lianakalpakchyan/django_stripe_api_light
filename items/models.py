from django.db import models

from items.enums import CurrencyEnum


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CurrencyEnum.choices, default=CurrencyEnum.USD)

    def __str__(self):
        return self.name


class Discount(models.Model):
    percent_off = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.percent_off}%"


class Tax(models.Model):
    display_name = models.CharField(max_length=100)
    inclusive = models.BooleanField(default=False)
    percentage = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.display_name


class Order(models.Model):
    order_code = models.CharField(max_length=11, unique=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, related_name="discount", null=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, related_name="tax", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_code


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in order {self.order.order_code}"
