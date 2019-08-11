from django.conf.urls import include
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views.users import *
from .views.lists import *
from .views.products import *


urlpatterns = [
    path('register', registration, name='registration'),
    path('login', obtain_auth_token, name='login'),
    path('logout', logout, name='login'),
    path('lists/', include([
        path('list', ListsList.as_view(), name='ListsList'),
        path('<int:pk>', ListDetail.as_view(), name='ListDetail'),
    ])),
    path('products/', include([
        path('add-to-store', add_to_product, name='add_to_product'),
        path('add-to-wishlist', add_to_wishlist, name='add_to_wishlist'),
        path('price-details/<int:pk>', ProductPriceDetail.as_view(), name='ProductDetail'),
        path('price-category', change_price_category, name='change_price_category'),
        path('average-price', get_average_price, name='get_average_price')
    ])),
    path('price/', include([
        path('detail/<int:pk>', PriceDetail.as_view(), name='ProductDetail'),
    ])),
]