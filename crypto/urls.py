from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("exchange/", exchange, name="exchange"),
    path("order/", deal, name="deal"),
    path("cancel/", cancel, name="cancel"),
    path("error/", error, name="error"),
    path("success/", success, name="success"),
    path("confirm/", confirm, name="confirm"),
    path("check_status/", check_status, name="check_status")
]
