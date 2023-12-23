from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.items, name='items'),
    path('item/<item_id>', views.item, name='item'),
    path('buy/<item_id>', views.buy, name='buy'),
    path('cart', views.cart, name='cart'),
    path('cart_count', views.cart_count, name='cart_count'),
    path('order_item/<item_id>', views.order_item, name='order_item'),
    path('order_item/add/<item_id>', views.order_item_add, name='order_item_add'),
    path('order_item/remove/<item_id>', views.order_item_remove, name='order_item_remove'),
    path('checkout/<order_id>', views.checkout, name='checkout'),
    path('payment_intent/<order_id>', views.payment_intent, name='payment_intent'),
    path('success', views.success, name='succes'),
    path('cancel', views.cancel, name='cancel'),
]