from django.contrib import admin
from .models import Product_detail, Category, Product

# Register your models here.


class Product_detailAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'rating',
        'image',
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'size',
        'price',
        'stock',
    )


admin.site.register(Product_detail, Product_detailAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
