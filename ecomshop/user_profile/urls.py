from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('add_address/', views.add_address, name='add_address'),
    path('update_address/', views.update_address, name='update_address'),
    path('adresses/', views.addresses, name='addresses'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),

]
