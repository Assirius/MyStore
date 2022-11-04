from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('products/', views.Products.as_view(), name='products'),
    path('category/<int:category_pk>/', views.ProductsByCategory.as_view(), name='category'),
    path('basket-add/<int:product_id>/', views.BasketAdd.as_view(), name='basket-add'),
    path('basket-delete/<int:basket_pk>/', views.BasketDelete.as_view(), name='basket-delete')
]