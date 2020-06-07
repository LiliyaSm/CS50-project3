from django.db import models


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
    # style = models.CharField(max_length=10, choices=STYLES)
    priceForSmall = models.DecimalField(max_digits=6, decimal_places=2)
    priceForLarge = models.DecimalField(max_digits=6, decimal_places=2, null=True)



    def __str__ (self):
        return f"{self.name} {self.group}"


#shopping cart
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
