from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("privacy-policy", views.privacy, name="privacy"),
    path("cookie-policy", views.cookie, name="cookie"),
    path("terms", views.terms, name="terms"),
    path("refund-policy", views.refund, name="refund")
]
