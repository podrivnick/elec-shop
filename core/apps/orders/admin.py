from django.contrib import admin

from .models import (
    OrderItem,
    Orders,
)


# class OrdersAdmin(admin.ModelAdmin):
#     list_display = ('user', 'name_receiver', 'surname_receiver', 'data_created_order', 'phone_number',
#                     'required_delivery', 'delivery_address', 'payment_on_get', 'has_paid', 'status',
#                     'email', 'total_price')
#
# class OrdersItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'product', 'name', 'price', 'quantity',
#                     'created_timestamp')
#
#
# admin.site.register(Orders, OrdersAdmin)
# admin.site.register(OrderItem, OrdersItemAdmin)


class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = "product", "name", "price", "quantity"
    search_fields = (
        "product",
        "name",
    )
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "name", "price", "quantity"
    search_fields = (
        "order",
        "product",
        "name",
    )


class OrderTabulareAdmin(admin.TabularInline):
    model = Orders
    fields = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "data_created_order",
    )

    search_fields = (
        "requires_delivery",
        "payment_on_get",
        "is_paid",
        "data_created_order",
    )
    readonly_fields = ("data_created_order",)
    extra = 0


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "required_delivery",
        "status",
        "payment_on_get",
        "has_paid",
        "data_created_order",
        "phone_number",
    )

    search_fields = (
        "id",
        "status",
        "name_receiver",
        "surname_receiver",
        "phone_number",
        "email",
    )
    readonly_fields = ("data_created_order",)
    list_filter = (
        "required_delivery",
        "status",
        "payment_on_get",
        "has_paid",
    )
    inlines = (OrderItemTabulareAdmin,)
