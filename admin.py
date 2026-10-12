
from django.contrib import admin
from .models import Menu, Orders


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'phone',
        'total_amount',
        'order_date',
        'status',
    )

    search_fields = ('customer_name', 'phone')
    list_editable = ('status',)
    ordering = ('-id',)