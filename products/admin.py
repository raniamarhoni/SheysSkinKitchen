from django.contrib import admin
from .models import Product, Category, Variation

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'rating',
        'image',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class Variation_Admin(admin.ModelAdmin):
    list_display = (
        'product',
        'size',
        'price',
        'stock',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Variation, Variation_Admin)
