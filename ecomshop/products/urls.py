from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('category/<int:category_id>/', views.product_list, name="product_list"),
    path('product/<int:product_id>/', views.product_view, name='product_view'),

]
