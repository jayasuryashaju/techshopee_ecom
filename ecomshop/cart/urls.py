from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add-to-wishlist/<int:product_id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist_detail/', views.wishlist_detail, name='wishlist_detail'),
    path('remove-from-wishlist/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('check_stock/', views.check_stock, name='check_stock'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),


    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),

    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('proceed_to_pay/', views.proceed_to_pay, name='proceed_to_pay'),
    path('orders/<int:order_id>/', views.order_details, name='order_details'),
    path('cancel_order', views.cancel_order, name='cancel_order'),
    path('order_return', views.order_return, name='order_return'),

    path('orders/<int:order_id>/invoice/', views.download_invoice, name='download_invoice'),

]
