from django.conf import settings
from django.db import models

from apps.products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'سلة {self.user.username}'

    class Meta:
        verbose_name = 'سلة تسوق'
        verbose_name_plural = 'سلال التسوق'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.quantity} × {self.product.name}'

    class Meta:
        verbose_name = 'عنصر سلة'
        verbose_name_plural = 'عناصر السلة'
        unique_together = [['cart', 'product']]
