
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
# from django.http import JsonResponse

def index(request):

    items = Item.objects.exclude(
        Q(group__dishType="Toppings") | Q(group__dishType="Extras"))
    context = {
        "user": request.user,
        "items": items,
    }
    return render(request, "menu/index.html", context)

@login_required
def add_to_cart(request):
    """adding items on the main page"""
    item_id = request.POST.get("id", "")
    priceType = request.POST.get("price", "")
    toppings = request.POST.get("toppings", "")    

    user = request.user
    item = get_object_or_404(Item, pk=item_id)

    size = "Large"
    if priceType == "priceForSmall":
        if not getattr(item, "priceForLarge"):
            size = "One size"
        else:
            size = "Small"
    
    cart, created = Cart.objects.get_or_create(user=request.user, confirmed = False)
    
    if toppings and len(toppings) > 0:
        toppings = json.loads(toppings)
        count = 0
        for value in toppings.values():
            count += int(value)
        try:
            #try to get price depending on the quantity.
            topping_price = get_object_or_404(ToppingsPrice,
            item=item, toppingQuantity=count)
            price = getattr(topping_price, priceType)
            # otherwise get dish price
        except Exception as e:
            print(e)
            price = getattr(item, priceType)

        order = ItemOrder(
            item=item, cart=cart, size=size, quantity = 1)
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
        # price for small or large
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


@login_required
def delete_item(request):
    '''delete items from cart on the cart page'''
    user = request.user
    id = request.POST.get("id", "")
    item = ItemOrder.objects.get(cart__user=user,  cart__confirmed=False, id=id)
    item.delete()

    if ItemOrder.objects.filter(cart__user=user,  cart__confirmed=False).count() == 0:
        last_one=True
    else:
        last_one=False

    cart = Cart.objects.get(user=user, confirmed=False)
    response_data = {"new_total": cart.total, "last_one": last_one}
    return HttpResponse(
        json.dumps(response_data, cls=DecimalEncoder),
        content_type="application/json"
    )


# shopping_cart.items.remove(item)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


@login_required

def update_cart(request):
    """changing items amount on the cart page"""
    user = request.user
    line_id = request.POST.get("id", "")
    new_amount = int(request.POST.get("amount", ""))
    changed_item = ItemOrder.objects.get(cart__user=user,  cart__confirmed=False, id=line_id)
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
        return render(request, "menu/cart.html", {"total": 0.00})
    items_user = ItemOrder.objects.filter(
        cart__user=user, cart__confirmed = False).exclude(Q(item__group__dishType="Toppings") | Q(item__group__dishType="Extras"))
         
    total = Cart.objects.get(user=user, confirmed=False).total
    items = items_user.select_related('item')

   
    context = {
        "itemorders": items,
        "total": total,
        "unconfirmed": True
    }
    return render(request, "menu/cart.html", context)


@login_required

def confirm_cart(request):
    """function invokes after pressing "confirm" button"""

    user = request.user
    cart = Cart.objects.get(user=user, confirmed=False)
    if not cart.total:
        return render(request, "menu/cart.html")
    cart.confirmed = True
    cart.order_date = datetime.datetime.now()
    cart.save()
    return HttpResponse(
        content_type="application/json"
    )


@login_required

def order_history(request):
    carts = Cart.objects.filter(user=request.user, confirmed=True).all()
    
    context = {
        "carts": carts
    }
    return render(request, "menu/orders_history.html", context)


@login_required(login_url='login')
def order_detail (request, id):
    """page with old confirmed order"""
    user = request.user
    items_user = ItemOrder.objects.filter(
        cart__user=user, cart__id = id).exclude(Q(item__group__dishType="Toppings") | Q(item__group__dishType="Extras"))
    cart_id = id

    total = Cart.objects.get(user=user, id=id).total
    items = items_user.select_related('item')
    # order = Cart.objects.get_object_or_404(user=request.user, cart__id=id)
    return render(request, "menu/cart.html", {'itemorders': items, "total": total, "unconfirmed": False, "cart_id": cart_id})


@login_required(login_url='login')
def order_repeat(request, id):

    #delete cart if it already exsists

    try:
        cart = Cart.objects.get(user=request.user, confirmed=False)
        cart.delete()
    except Cart.DoesNotExist:
        pass

    new_cart = copy.deepcopy(Cart.objects.get(user=request.user, id=id))
    new_cart.pk = None
    new_cart.order_date = datetime.datetime.now()
    new_cart.confirmed = False
    new_cart.save()

    # items = ItemOrder.objects.filter(cart__user=request.user, cart__pk=id)
    # new_items = copy.deepcopy(items)
    # new_items.update(cart=new_cart)

    items = copy.copy(ItemOrder.objects.filter(
        cart__user=request.user, cart__pk=id))


    #items.update(id=None)

    for i in items:
        i.pk = None
        i.cart_id = new_cart.pk
    ItemOrder.objects.bulk_create(items)

    return redirect("cart")

        


# share = Share.objects.get(shared_user_id=log_id)


    #
    # book = Book.objects.get(pk=book_id)
    # try:
    #     preexisting_order = BookOrder.objects.get(book=book, cart=self)
    #     if preexisting_order.quantity > 1:
    #         preexisting_order.quantity -= 1
    #         preexisting_order.save()
    #     else:
    #         preexisting_order.delete()
    # except BookOrder.DoesNotExist:
    #     pass
