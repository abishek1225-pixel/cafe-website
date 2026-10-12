
from django.db import models


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    image = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'menu'

    def __str__(self):
        return self.name


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='Pending')

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return f"Order {self.id}"