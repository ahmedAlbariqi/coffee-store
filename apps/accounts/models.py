from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمون'


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    street = models.TextField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.full_name} - {self.city}'

    class Meta:
        verbose_name = 'عنوان'
        verbose_name_plural = 'العناوين'
