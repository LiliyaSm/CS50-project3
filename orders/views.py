
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Item, Cart, ItemOrder
from django.contrib import messages

# from django.http import JsonResponse

# Create your views here.
def index(request):

    items = Item.objects.all()
    
    # p.get_shirt_size_display()
    context = {
        "user": request.user,
        "items": Item.objects.all() 
    }

    return render(request, "menu/index.html", context)


def getEvents (request):
    print(request.GET.get("type", ""))
    return False



def add_to_cart(request):
    item_id = request.POST.get("id", "")
    priceType = request.POST.get("price", "")
    amount = request.POST.get("amount", "")

    item = get_object_or_404(Item, pk=item_id)

    user = request.user

    # price for small or large
    price = getattr(item, priceType)
    print(price, item_id, amount, user)


    cart, created = Cart.objects.get_or_create(user=request.user)
    order, created = ItemOrder.objects.get_or_create(
        item=item, cart=cart, price=price)

    order.quantity += int(amount)
    order.calc_price = order.quantity * price
    order.save()
    # messages.success(request, "Cart updated!")
    return False


    #    return HttpResponse(
    #        json.dumps(response_data),
    #        content_type="application/json"
    #    )



def remove_from_cart(request):
    '''delete items from cart on cart page'''

    order = get_object_or_404(ItemOrder, pk=item_id)

def cart(request):
    """shopping cart page with order"""

    user = request.user
    items_o = ItemOrder.objects.filter(cart__user=user)
    total = Cart.objects.get(user=user).total
    items_1 = items_o.select_related('item')
    # for p in items_1:
    #     print(p.cart.total)
    print(total)
    # quantity = items_o.values("total")
   
    context = {
        "itemorders": items_1,
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
