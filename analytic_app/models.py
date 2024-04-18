from django.db import models
from datetime import date, datetime



class Bakery_address(models.Model):
    bakery_address = models.CharField(max_length=100, default='не указан')


class Cost(models.Model):
    cost_name = models.CharField(max_length=100, default='не указан')


class Product(models.Model):
    product_name = models.CharField(max_length=100, default='не указан')

# class Month(models.Model):
#     month = models.CharField(max_length=30, default='не указан')

class Revenue_daily(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    month = models.IntegerField(default=datetime.now().month)
    bakery_address = models.ForeignKey(Bakery_address, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_sum = models.DecimalField(max_digits=8, decimal_places=2)


class Costs_by_month(models.Model):
    cost_name = models.ForeignKey(Cost, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    month = models.IntegerField(default=datetime.now().month)
    bakery_address = models.ForeignKey(Bakery_address, on_delete=models.CASCADE)
    amount_of_costs = models.DecimalField(max_digits=8, decimal_places=2)
