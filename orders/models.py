from django.db import models

# Create your models here.
class dishType(models.Model):
    dishType = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.dishType}"

class Item(models.Model):
    name = models.CharField(max_length=64)
    group = models.ForeignKey(
        dishType, on_delete=models.CASCADE, related_name="group", null=True)
    priceForSmall = models.DecimalField(max_digits=6, decimal_places=2)
    priceForLarge = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__ (self):
        return f"{self.name} {self.group}"


