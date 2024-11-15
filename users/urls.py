from django.urls import path
from .views import *

urlpatterns = [
    path('logout/', user_logout, name='logout'),
    path('sign-up/', register, name='sign-up'),
    path('sign-in/', user_login, name='sign-in'),

]