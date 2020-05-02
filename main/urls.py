from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('?P<str:category>', views.index, name='index'),
    path('products/<int:product_id>', views.product, name='product'),
    path('cart', views.cart_page, name='cart_page'),
    path('cart/all', views.cart_details, name='cart_details'),
    path('cart/add/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>', views.remove_from_cart, name='remove_from_cart'),
    path('order', views.make_order, name='make_order')
]
