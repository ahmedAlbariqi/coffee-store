from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add/<slug:slug>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('update/<int:pk>/', views.UpdateCartItemView.as_view(), name='update_item'),
    path('remove/<int:pk>/', views.RemoveCartItemView.as_view(), name='remove_item'),
    path('clear/', views.ClearCartView.as_view(), name='clear_cart'),
]
