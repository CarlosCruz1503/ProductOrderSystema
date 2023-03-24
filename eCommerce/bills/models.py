from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.IntegerField()
    stock = models.IntegerField()
    ordered = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    date = models.DateTimeField()
    client = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(f"El cliente{self.client}, realizo una orden a las{self.date}")


class OrderDetail(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=False, blank=False
    )
    quantity = models.IntegerField()
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False
    )


# Create your models here.
