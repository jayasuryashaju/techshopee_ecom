from django.urls import path
from . import views

app_name = 'ecom_admin'

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('user_details', views.user_details, name='user_details'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('add_user', views.add_user, name='add_user'),
    path('edit_user/<str:pk>/', views.edit_user, name='edit_user'),
    path('block_user/<str:pk>/', views.block_user, name='block_user'),
    path('delete_user/<str:username>/', views.delete_user, name='delete_user'),

    path('categories_view', views.categories_view, name='categories_view'),
    path('add_category', views.add_category, name='add_category'),
    path('category/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),

    path('products/', views.product_list, name='product_list'),
    path('add-product/<int:category_id>/', views.add_product, name='add_product'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('product/<int:pk>/', views.product_details, name='product_details'),

    path('order_details/', views.order_details, name='order_details'),
    path('order_details_product/<int:order_id>/', views.order_details_product, name='order_details_product'),
    path('change_order_status/<int:order_id>/', views.change_order_status, name='change_order_status'),

    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('coupon_list/', views.coupon_list, name='coupon_list'),
    path('edit_coupon/<int:pk>', views.edit_coupon, name='edit_coupon'),
    path('delete_coupon/<int:pk>', views.delete_coupon, name='delete_coupon'),

    path('offers/', views.offers, name='offers'),
    path('add_category_offer/', views.add_category_offer, name='add_category_offer'),
    path('edit_category_offer/<category_id>', views.edit_category_offer, name='edit_category_offer'),
    path('delete_category_offer/<int:id>', views.delete_category_offer, name='delete_category_offer'),
    path('apply_category_offer/<int:category_offer_id>', views.apply_category_offer, name='apply_category_offer'),
    path('deactivate_offer/<int:category_offer_id>', views.deactivate_offer, name='deactivate_offer'),
    path('add_product_offer', views.add_product_offer, name='add_product_offer'),
    path('delete_product_offer/<int:id>', views.delete_product_offer, name='delete_product_offer'),
    path('apply_product_offer/<int:product_offer_id>', views.apply_product_offer, name='apply_product_offer'),
    path('edit_product_offer/<product_id>', views.edit_product_offer, name='edit_product_offer'),
    path('deactivate_product_offer/', views.deactivate_product_offer, name='deactivate_product_offer'),

    path('sales_report/', views.sales_report, name='sales_report'),
    path('by_date/', views.by_date, name='by_date'),
    path('generates_sales_report/', views.generates_sales_report.as_view(), name='generates_sales_report'),
    path('by_month/', views.by_month, name='by_month'),
    path('by_year/', views.by_year, name='by_year'),
    path('download_docx/', views.download_docx, name='download_docx'),\

    path('banner_list/', views.banner_list, name='banner_list'),
    path('banner_add/', views.banner_add, name='banner_add'),
    path('banner_edit/<int:banner_id>/', views.banner_edit, name='banner_edit'),
    path('banner_delete/<int:banner_id>/', views.banner_delete, name='banner_delete'),


]
