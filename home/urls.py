from .views import *
from django.urls import path

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('signup',signup, name='signup'),
    path('login', dologin, name='dologin'),
    path('logout', dologout, name='dologout'),
    path('search', Search.as_view(), name='search'),
    path('detail/<slug>', Product_detail.as_view(), name='detail'),
    path('review', review, name='review'),
    path('category/<slug>', Cat.as_view(), name='category'),
    path('add_cart/<slug>', add_cart, name='add_cart'),
    path('car', Car.as_view(), name='car'),
    path('reduce/<slug>', reduce_quantity, name='reduce'),
    path('del/<slug>', delete_cart, name='del'),
    path('check', Check.as_view(), name='check'),
    path('order', orderform, name='order'),


]