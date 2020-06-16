
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Item, Cart, ItemOrder
from django.http import HttpResponse
import json
import decimal
# from django.http import JsonResponse

# Create your views here.
def index(request):

    items = Item.objects.exclude(group__dishType="Toppings")
    for item in items:
        for linkedItem in item.items.all():
            print(linkedItem)

    
    toppings = ["Pepperoni",
                "Sausage",
                "Mushrooms",
                "Onions"]
    # p.get_shirt_size_display()
    context = {
        "user": request.user,
        "items": items,
        "toppings": toppings
    }

    return render(request, "menu/index.html", context)


def getEvents (request):
    print(request.GET.get("type", ""))
    return False



def add_to_cart(request):
    """adding items on the main page"""
    item_id = request.POST.get("id", "")
    priceType = request.POST.get("price", "")
    # amount = request.POST.get("amount", "")
    user = request.user

    item = get_object_or_404(Item, pk=item_id)

    size = "Large"
    if priceType == "priceForSmall":
        if not getattr(item, "priceForLarge"):
            size = "One size"
        else:
            size = "Small"


    # price for small or large
    price = getattr(item, priceType)
    print(price, item_id, user)
    

    cart, created = Cart.objects.get_or_create(user=request.user)
    order, created = ItemOrder.objects.get_or_create(
        item=item, cart=cart, price=price, size=size)

    order.quantity += 1
    order.calc_price += price
    order.save()

    cart.total +=  price
    cart.save()
    return HttpResponse(
        content_type="application/json"
    )




def delete_item(request):
    '''delete items from cart on the cart page'''
    user = request.user
    id = request.POST.get("id", "")
    item = ItemOrder.objects.get(cart__user=user, id=id)
    item.delete()
    cart = Cart.objects.get(user=user)
    response_data = {"new_total": cart.total}
    return HttpResponse(
        json.dumps(response_data, cls=DecimalEncoder),
        content_type="application/json"
    )

    # deleted_item.remove()
    # Cart.objects.get(user=user)

# shopping_cart.items.remove(item)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def update_cart(request):
    """changing items amount on the cart page"""
    user = request.user
    line_id = request.POST.get("id", "")
    new_amount = int(request.POST.get("amount", ""))
    changed_item = ItemOrder.objects.get(cart__user=user, id=line_id)
    cart = Cart.objects.get(user=user)
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
    new_total = Cart.objects.get(user=user).total
    response_data = {"new_price": new_price, "new_total": new_total}
    return HttpResponse(
        json.dumps(response_data, cls=DecimalEncoder),
        content_type="application/json"
    )

def cart(request):
    """shopping cart page with order"""

    user = request.user
    if not Cart.objects.filter(user=user).exists():
        return render(request, "menu/cart.html", {"total": 0.00})
    items_user = ItemOrder.objects.filter(cart__user=user)
    total = Cart.objects.get(user=user).total
    items = items_user.select_related('item')
    # for p in items_1:
    #     print(p.cart.total)

   
    context = {
        "itemorders": items,
        "total": total
    }
    return render(request, "menu/cart.html", context)





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
