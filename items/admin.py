from django.contrib import admin

from items.models import Item, Discount, Tax, Order, OrderItem


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'currency')


admin.site.register(Item, ItemAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'percent_off')


admin.site.register(Discount, DiscountAdmin)


class TaxAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'inclusive', 'percentage')
    list_editable = ('inclusive',)


admin.site.register(Tax, TaxAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'created_at', 'updated_at')


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'item', 'quantity')


admin.site.register(OrderItem, OrderItemAdmin)
