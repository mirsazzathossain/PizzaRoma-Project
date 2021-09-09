from typing import ValuesView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("privacy-policy", views.privacy, name="privacy"),
    path("cookie-policy", views.cookie, name="cookie"),
    path("terms", views.terms, name="terms"),
    path("refund-policy", views.refund, name="refund"),
    path("pizza/<int:id>", views.details, name="details"),
    path("menu", views.menu, name="menu"),
    path('update-item', views.updateItem, name='update-item'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
]
