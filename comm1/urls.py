# -*- coding: utf-8 -*-

from django.urls import path,include
from . import views

from django.conf.urls.static import static

urlpatterns=[
    path('',views.index,name='index'),
    path('Category_list',views.Category_list,name='category'),
    path('Category_product_list/<int:id>',views.Category_product_list,name='Category_product_list'),
    path('Brand_list',views.Brand_list,name='Brand'),
    path('Brand_product_list/<int:id>',views.Brand_product_list,name='Brand_product_list'),
    path('productlist',views.productlist,name='productlist'),
    path('products/<int:id>',views.products,name='products'),
    path('filter_data',views.filter_data,name='filter_data'),
    path('addtocart',views.addtocart,name='addtocart'),
    path('cart',views.cart,name='cart'),
    path('update-cart',views.updatecart,name='update-cart'),
    path('accounts/signup',views.signup,name='signup'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    
    path('checkout',views.checkout,name='checkout')
    ]