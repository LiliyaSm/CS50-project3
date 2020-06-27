from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from .models import Item, Cart, ItemOrder, ToppingsPrice
import json
import decimal
import datetime
import copy
from django.contrib import messages


@login_required(login_url='login')
def index(request):
    """rendering items on the main page"""

    items = Item.objects.exclude(
        Q(group__dishType="Toppings") | Q(group__dishType="Extras"))
    return render(request, "orders/index.html",{ "items": items})


@login_required(login_url='login')
def add_to_cart(request):
    """adding items on the main page"""
    item_id = request.POST.get("id", "")
    priceType = request.POST.get("price", "")
    toppings = request.POST.get("toppings", "")

    item = get_object_or_404(Item, pk=item_id)

    # if item has only "small" price its size is "one size"
    if priceType == "priceForSmall":
        if not getattr(item, "priceForLarge"):
            size = "One size"
        else:
            size = "Small"
    else:
        size = "Large"


    cart, created = Cart.objects.get_or_create(
        user=request.user, confirmed=False)

    if toppings and len(toppings) > 0:
        toppings = json.loads(toppings)
        count = 0
        for value in toppings.values():
            count += int(value)

            #try to get price for topping depending on the quantity.
        try:
            topping_price = get_object_or_404(ToppingsPrice,
                                              item=item, toppingQuantity=count)
            price = getattr(topping_price, priceType)
            # otherwise get topping own price
        except Exception as e:
            print(e)
            price = getattr(item, priceType)
        # create main dish
        order = ItemOrder(
            item=item, cart=cart, size=size, quantity=1)
        order.save()

        for key, value in toppings.items():
            item_top = get_object_or_404(Item, pk=key)
            price_top = getattr(item_top, priceType)*int(value)
            price += price_top
            # place topping in the order
            topping = ItemOrder(
                item=item_top, cart=cart, quantity=value, price=getattr(item_top, priceType))
            topping.save()
            # link main dish and topping
            order.toppings.add(topping)

        order.price = price
        order.calc_price += price
        order.save()

    else:
        # get price for small or large
        price = getattr(item, priceType)
        order, created = ItemOrder.objects.get_or_create(
            item=item, cart=cart, price=price, size=size)
        order.quantity += 1
        order.calc_price += price
        order.save()

    cart.total += price
    cart.save()
    return HttpResponse(
        content_type="application/json"
    )


@login_required(login_url='login')
def delete_item(request):
    '''delete item with related toppings from cart on the cart page'''
    user = request.user
    id = request.POST.get("id", "")
    item = ItemOrder.objects.get(
        cart__user=user,  cart__confirmed=False, id=id)
    item.delete()

    if ItemOrder.objects.filter(cart__user=user,  cart__confirmed=False).count() == 0:
        last_one = True
    else:
        last_one = False

    cart = Cart.objects.get(user=user, confirmed=False)
    response_data = {"new_total": cart.total, "last_one": last_one}
    return HttpResponse(
        json.dumps(response_data, cls=DecimalEncoder),
        content_type="application/json"
    )


# class to serialize a Decimal object
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


@login_required(login_url='login')
def update_cart(request):
    """changing items amount on the cart page"""
    user = request.user
    line_id = request.POST.get("id", "")
    new_amount = int(request.POST.get("amount", ""))
    changed_item = ItemOrder.objects.get(
        cart__user=user,  cart__confirmed=False, id=line_id)
    cart = Cart.objects.get(user=user, confirmed=False)
    new_price = new_amount * changed_item.price

    if changed_item.quantity > new_amount:
        cart.total -= changed_item.price
    elif changed_item.quantity < new_amount:
        cart.total += changed_item.price
    else:
        return HttpResponse(
            content_type="application/json"
        )

    # rewrite amount and total price for this product
    changed_item.quantity = new_amount
    changed_item.calc_price = new_price
    changed_item.save()

    cart.save()
    new_total = Cart.objects.get(user=user, confirmed=False).total
    response_data = {"new_price": new_price, "new_total": new_total}
    return HttpResponse(
        json.dumps(response_data, cls=DecimalEncoder),
        content_type="application/json"
    )


@login_required(login_url='login')
def cart(request):
    """shopping cart page with order"""

    user = request.user
    if not Cart.objects.filter(user=user, confirmed=False).exists():
        return render(request, "orders/cart.html", {"total": 0.00})
    items_user = ItemOrder.objects.filter(
        cart__user=user, cart__confirmed=False).exclude(Q(item__group__dishType="Toppings") | Q(item__group__dishType="Extras"))

    total = Cart.objects.get(user=user, confirmed=False).total
    items = items_user.select_related('item')

    context = {
        "itemorders": items,
        "total": total,
        "unconfirmed": True
    }
    return render(request, "orders/cart.html", context)


@login_required(login_url='login')
def confirm_cart(request):
    """function invokes after pressing "confirm" button"""

    user = request.user
    cart = Cart.objects.get(user=user, confirmed=False)
    if not cart.total:
        return render(request, "orders/cart.html")
    cart.confirmed = True
    cart.order_date = datetime.datetime.now()
    cart.save()
    messages.add_message(request, messages.INFO, 'Your order is confirmed!')

    return redirect("cart")


@login_required(login_url='login')
def order_history(request):
    """rendering order history"""

    carts = Cart.objects.filter(user=request.user, confirmed=True).all()
    return render(request, "orders/orders_history.html", {
        "carts": carts
    })


@login_required(login_url='login')
def order_detail(request, id):
    """page with old confirmed order"""
    user = request.user
    items_user = ItemOrder.objects.filter(
        cart__user=user, cart__id=id).exclude(Q(item__group__dishType="Toppings") | Q(item__group__dishType="Extras"))

    total = Cart.objects.get(user=user, id=id).total
    items = items_user.select_related('item')
    return render(request, "orders/cart.html", {'itemorders': items, "total": total, "unconfirmed": False, "cart_id": id})


@login_required(login_url='login')
def order_repeat(request, id):
    """repeating old order"""

    #delete current cart if it exsists
    try:
        cart = Cart.objects.get(user=request.user, confirmed=False)
        cart.delete()
    except Cart.DoesNotExist:
        pass
    # make a copy of cart
    new_cart = copy.deepcopy(Cart.objects.get(user=request.user, id=id))
    new_cart.pk = None
    new_cart.order_date = datetime.datetime.now()
    new_cart.confirmed = False
    new_cart.save()

    items = copy.copy(ItemOrder.objects.filter(
        cart__user=request.user, cart__pk=id))

    ThroughModel = ItemOrder.toppings.through

    old_items = copy.copy(ItemOrder.objects.filter(
        cart__user=request.user, cart__pk=id))

    # keep track of already added items
    processed_items = []

    for i in old_items:
        if i.pk not in processed_items:
            processed_items.append(i.pk)
            toppings = copy.copy(i.toppings.all())
            i.pk = None
            i.cart_id = new_cart.pk
            i.save()
    # make a copy of related toppings
            if toppings:
                for topping in toppings:
                    processed_items.append(topping.pk)
                    topping.pk = None
                    topping.cart_id = new_cart.pk
                    topping.save()
                    ThroughModel.objects.create(
                        from_itemorder_id=i.pk, to_itemorder_id=topping.pk
                    )

    messages.add_message(request, messages.INFO,
                         'Your previous order was copied to your cart!')

    return redirect("cart")
