from .models import *


def cartData(request):
    costumer = request.user.costumer

    order = Order.objects.filter(costumer=costumer, complete=False)
    if not order.exists():
        order = Order.objects.create(costumer=costumer, complete=False)
    else:
        order = order.last()

    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    return {'items': items, 'order': order, 'cartItems': cartItems}
