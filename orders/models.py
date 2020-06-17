from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from decimal import Decimal


# Create your models here.
class dishType(models.Model):
    dishType = models.CharField(max_length=64)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.dishType}"


class Item(models.Model):
    name = models.CharField(max_length=64)
    group = models.ForeignKey(
        dishType, on_delete=models.CASCADE, related_name="group", null=True)
    #connection beetwen dish and topping asymmetr, we need add toppings to dish, not vice versa
    items = models.ManyToManyField("self", symmetrical=False, blank=True)
    hasToppings = models.BooleanField(default=False)
    priceForSmall = models.DecimalField(max_digits=6, decimal_places=2)
    priceForLarge = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal(0))

    def __str__ (self):
        return f"{self.name} {self.group}"


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user", null=False)
    order_date = models.DateField(null=True)  # auto_now_add=True
    total = models.DecimalField(default=Decimal(0), max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Item, through='ItemOrder')



    # payment_type = models.CharField(max_length=100, null=True)
    # payment_id = models.CharField(max_length=100, null=True)


    def __str__(self):
        # return "User: {} has items in their cart. Their total is ${}".format(self.user, self.total)
        return f"{self.user}"

    

#     def add_to_cart(self, book_id):
#         item = get_object_or_404(Item, pk=item_id)


class ItemOrder(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="product")
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart")

    toppings = models.ManyToManyField("self", symmetrical=False, blank=True)
    quantity = models.PositiveIntegerField(default=0)  # default = 1
    price = models.DecimalField(default=Decimal(0), max_digits=10, decimal_places=2)
    calc_price = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal(0))
    size = models.CharField(max_length=15, default="One size")


    def __str__(self):
        return f"{self.item}"


# @receiver(post_save, sender=ItemOrder)
# def update_cart(sender, instance, **kwargs): 
#     instance.cart.total += instance.calc_price
#     instance.cart.save()

    # instance.cart.count += instance.quantity
    # instance.cart.updated = datetime.now()

@receiver(pre_delete, sender=ItemOrder)
def delete_item(sender, instance, **kwargs):
    # before main dish removing from cart delete all related topping objects
    instance.toppings.all().delete()

    instance.cart.total -= instance.calc_price
    instance.cart.save()






# class Order(models.Model):
#     dishType = models.CharField(max_length=64)
# class CartItem(models.Model):
#  cart_id = models.CharField(max_length=50)
#  date_added = models.DateTimeField(auto_now_add=True)
#  quantity = models.IntegerField(default=1)
#  product = models.ForeignKey('catalog.Product', unique=False)

#  class Meta:
#  db_table = 'cart_items'
#  ordering = ['date_added']

#  def total(self):
#  return self.quantity * self.product.price

#  def name(self):
#  return self.product.name

#  def price(self):
#  return self.product.price


# www.it-ebooks.info
# CHAPTER 4 ■ THE SHOPPING CART
# 83


# def get_absolute_url(self):
#  return self.product.get_absolute_url()
#  def augment_quantity(self, quantity):
#  self.quantity = self.quantity + int(quantity)
#  self.save()
