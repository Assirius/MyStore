from django.contrib import admin
from products import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Basket)
class BasketAdmin(admin.ModelAdmin):
    pass