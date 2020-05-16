from django.utils import timezone
from django.db import models
from customer.models import Customer


class Invoice(models.Model):
    id = models.CharField(primary_key=True, max_length=8, editable=False)
    customer_name = models.CharField(max_length=20, default='CASH')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    customer_address = models.CharField(max_length=30, blank=True)
    customer_phone = models.CharField(blank=True, max_length=10)
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    sub_total = models.FloatField(null=False)
    last_bal = models.IntegerField(default=0)
    p_and_f = models.FloatField(default=0)
    round_off = models.FloatField(default=0.0)
    total_amount = models.FloatField()
    amount_paid = models.IntegerField(default=0)
    current_bal = models.IntegerField(default=0)

    def __str__(self):
        return self.id


class Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50, blank=False)
    item_quantity = models.IntegerField(null=False)
    item_mrp = models.FloatField(null=False)
    item_discount = models.FloatField(default=0)
    item_sp = models.FloatField(null=False)
    item_total = models.FloatField(null=False)

    def __str__(self):
        return self.item_name
