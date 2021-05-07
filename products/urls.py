from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path(
        '<int:product_id>/<int:size_id>/', views.product_size,
        name='product_size'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/',
         views.delete_product, name='delete_product'),
    path('add/<int:product_id>/', views.add_size, name='add_size'),
    path('edit/<int:product_id>/<int:size_id>/',
         views.edit_size, name='edit_size'),
]
