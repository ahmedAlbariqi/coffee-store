from django.conf import settings
from django.db import models

from apps.products.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'قيد الانتظار'
        PROCESSING = 'processing', 'قيد التجهيز'
        SHIPPED = 'shipped', 'تم الشحن'
        DELIVERED = 'delivered', 'تم التوصيل'
        CANCELLED = 'cancelled', 'ملغي'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'طلب #{self.pk} - {self.full_name}'

    class Meta:
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def get_total_price(self):
        return self.quantity * self.product_price

    def __str__(self):
        return f'{self.quantity} × {self.product_name}'

    class Meta:
        verbose_name = 'عنصر طلب'
        verbose_name_plural = 'عناصر الطلب'
