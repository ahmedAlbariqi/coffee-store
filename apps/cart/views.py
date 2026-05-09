from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from apps.products.models import Product

from .models import Cart, CartItem


def _get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = _get_or_create_cart(self.request.user)
        items = cart.items.select_related('product').all()
        context['cart'] = cart
        context['items'] = items
        context['total'] = sum(item.get_total_price for item in items)
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug, is_active=True)
        cart = _get_or_create_cart(request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1},
        )

        if not created:
            new_quantity = item.quantity + 1
            if new_quantity > product.stock:
                messages.error(request, f'Only {product.stock} units of "{product.name}" are available.')
                return redirect('cart:cart')
            item.quantity = new_quantity
            item.save(update_fields=['quantity'])

        messages.success(request, f'"{product.name}" added to your cart.')
        return redirect('cart:cart')


class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)

        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            messages.error(request, 'Invalid quantity.')
            return redirect('cart:cart')

        if quantity <= 0:
            item.delete()
            messages.success(request, f'"{item.product.name}" removed from your cart.')
        elif quantity > item.product.stock:
            messages.error(request, f'Only {item.product.stock} units of "{item.product.name}" are available.')
        else:
            item.quantity = quantity
            item.save(update_fields=['quantity'])
            messages.success(request, 'Cart updated.')

        return redirect('cart:cart')


class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        product_name = item.product.name
        item.delete()
        messages.success(request, f'"{product_name}" removed from your cart.')
        return redirect('cart:cart')


class ClearCartView(LoginRequiredMixin, View):
    def post(self, request):
        cart = _get_or_create_cart(request.user)
        cart.items.all().delete()
        messages.success(request, 'Your cart has been cleared.')
        return redirect('cart:cart')
