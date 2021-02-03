from django.contrib import admin
from .models import Product, Category, Size

# Register your models here.


class SizeAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'size',
        'price',
        'stock',
    )

    ordering = ('sku',)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'image',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Size, SizeAdmin)
