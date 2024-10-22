from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.home,name="home"),
    path('cart/',views.cart,name="cart"),
    path('update_item/',views.updateItems,name="updateItems"),
    path('register/',views.register,name='register'),
     path('remove/<int:product_id>/',views.remove_from_cart, name='remove_from_cart'),
]
