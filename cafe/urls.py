from django.urls import path
from . import views

app_name = 'cafe'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('about/', views.about, name='about'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    # path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/modal/', views.product_modal, name='product_modal'),
    path('order/modal/', views.order_modal, name='order_modal'),
    path('order/create/', views.order_create, name='order_create'),
] 