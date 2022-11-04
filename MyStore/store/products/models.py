from django.db import models

from users.models import User


class ProductCategory(models.Model):

    title = models.CharField(max_length=64, unique=True, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    image = models.ImageField(upload_to='products_images/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    short_description = models.CharField(max_length=64, blank=True, verbose_name='Краткое описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return f'{self.title} | {self.category.title}'


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.title}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def sum(self):
        return self.quantity * self.product.price