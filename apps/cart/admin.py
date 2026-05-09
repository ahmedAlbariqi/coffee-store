from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_items_count', 'created_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

    @admin.display(description='عدد العناصر')
    def get_items_count(self, obj):
        return obj.items.count()
