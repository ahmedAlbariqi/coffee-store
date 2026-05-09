from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.products.models import Product

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, slug=kwargs['slug'], is_active=True)
        if request.user.is_authenticated:
            if Review.objects.filter(user=request.user, product=self.product).exists():
                messages.error(request, 'You have already reviewed this product.')
                return redirect('products:product_detail', slug=self.product.slug)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.product
        messages.success(self.request, 'Your review has been submitted.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.product.slug})


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('product')

    def form_valid(self, form):
        messages.success(self.request, 'Your review has been updated.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.object.product.slug})


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('product')

    def form_valid(self, form):
        messages.success(self.request, 'Your review has been deleted.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.object.product.slug})
