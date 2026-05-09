from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView

from apps.cart.models import Cart

from .models import Order, OrderItem


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    city = forms.CharField(max_length=100)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related('items__product')
        )


class CheckoutView(LoginRequiredMixin, FormView):
    form_class = CheckoutForm
    template_name = 'orders/checkout.html'

    def _get_cart_items(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return list(cart.items.select_related('product').all())

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not self._get_cart_items():
            messages.error(request, 'Your cart is empty.')
            return redirect('cart:cart')
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        user = self.request.user
        return {
            'full_name': user.get_full_name(),
            'email': user.email,
            'phone': getattr(user, 'phone', ''),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self._get_cart_items()
        context['items'] = items
        context['total'] = sum(item.get_total_price for item in items)
        return context

    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self._order_pk})

    def form_valid(self, form):
        items = self._get_cart_items()
        if not items:
            messages.error(self.request, 'Your cart is empty.')
            return redirect('cart:cart')

        total = sum(item.get_total_price for item in items)

        with transaction.atomic():
            order = Order.objects.create(
                user=self.request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                total_price=total,
            )
            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    product_price=item.product.price,
                    quantity=item.quantity,
                )
                for item in items
            ])
            Cart.objects.get(user=self.request.user).items.all().delete()

        self._order_pk = order.pk
        messages.success(self.request, f'Order #{order.pk} placed successfully.')
        return super().form_valid(form)


class OrderCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)

        if order.status != Order.Status.PENDING:
            messages.error(request, 'Only pending orders can be cancelled.')
            return redirect('orders:order_detail', pk=pk)

        order.status = Order.Status.CANCELLED
        order.save(update_fields=['status', 'updated_at'])
        messages.success(request, f'Order #{order.pk} has been cancelled.')
        return redirect('orders:order_list')
