from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('<int:pk>/cancel/', views.OrderCancelView.as_view(), name='order_cancel'),
]
