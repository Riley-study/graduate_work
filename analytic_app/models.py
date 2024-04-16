from django.db import models


class Bakery_address(models.Model):
    bakery_address = models.CharField(max_length=100)


class Profitability_by_product(models.Model):
    product_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    bakery_address = models.ForeignKey(Bakery_address, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_sum = models.DecimalField(max_digits=8, decimal_places=2)


class Costs_by_month(models.Model):
    cost_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    bakery_address = models.ForeignKey(Bakery_address, on_delete=models.CASCADE)
    amount_of_costs = models.DecimalField(max_digits=8, decimal_places=2)
