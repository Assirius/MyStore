from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from products import models

class ProductsMixin:
    categories_lst = models.ProductCategory.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)

class Index(View):
    def get(self, request):
        return render(request, template_name='products/index.html', context={'title': 'Store'})


class Products(ListView, ProductsMixin):
    model = models.Product
    template_name = 'products/products.html'
    context_object_name = 'products_lst'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Products, self).get_context_data(**kwargs)
        context['title'] = 'Store - Каталог'
        context['categories_lst'] = self.categories_lst
        return context

class ProductsByCategory(ListView, ProductsMixin):
    model = models.Product
    template_name = 'products/products.html'
    context_object_name = 'products_lst'
    paginate_by = 3

    def get_queryset(self):
        return models.Product.objects.filter(category_id=self.kwargs['category_pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsByCategory, self).get_context_data(**kwargs)
        category = models.ProductCategory.objects.get(pk=self.kwargs['category_pk'])
        context['title'] = category.title
        context['categories_lst'] = self.categories_lst
        return context


class BasketAdd(LoginRequiredMixin, View):

    def get(self, request, product_id):
        product = models.Product.objects.get(pk=product_id)
        baskets = models.Basket.objects.filter(user=request.user, product=product)

        if baskets.exists():
            baskets = baskets.first()
            baskets.quantity += 1
            baskets.save()

            return redirect('users:profile')

        else:
            models.Basket.objects.create(user=request.user, product=product, quantity=1)
            return redirect('users:profile')


class BasketDelete(LoginRequiredMixin, View):

    def get(self, request, basket_pk):
        basket = models.Basket.objects.get(pk=basket_pk)
        basket.delete()

        return redirect('users:profile')