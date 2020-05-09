from django.urls import path
from .views import *


urlpatterns = [
    path('', shop, name="shop"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('checkout/address/', checkoutAddress, name="checkoutAddress"),
    path('update_cart/', updateCart, name="updateCart"),
    path('update_address/', updateOrderAddress, name="updateOrderAddress"),
    path('address/<int:id>/edit', updateAddress, name='updateAddress'),
    path('addressShip/add', addShippingAddress, name='addShippingAddress'),
    path('addressInvoice/add', addInvoiceAddress, name='addInvoiceAddress'),
]

