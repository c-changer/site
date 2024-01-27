from django.urls import path
from .views import *

urlpatterns = [
    path('partners/', partners, name="partners"),
    path('reviews/', reviews, name="reviews"),
    path('contact/', contact, name="contact"),
    path('agreement/', agreement, name="agreement"),
    path('aml-agreement/', aml_agreement, name="aml-agreement"),
]
