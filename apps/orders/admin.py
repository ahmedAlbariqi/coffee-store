from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'status', 'total_price', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
