from django.db import models


# class Customer(models.Model):
#     cat_choices = [('G', 'General'), ('A', 'Category A'), ('B', 'Category B'), ('C', 'Category C')]
#
#     name = models.CharField(max_length=255, null=False)
#     firm_name = models.CharField(max_length=255, null=False)
#     address = models.TextField()
#     gstin = models.CharField(max_length=15, null=True)
#     primary_num = models.IntegerField(null=False)
#     secondary_num = models.IntegerField(null=True)
#     category = models.CharField(max_length=20, choices=cat_choices)
#
#     def __str__(self):
#         return self.name


class Invoice(models.Model):
    id = models.CharField(primary_key=True, max_length=8, editable=False)
    customer_name = models.CharField(max_length=20, default='CASH')
    customer_address = models.CharField(max_length=30, blank=True)
    customer_phone = models.CharField(blank=True, max_length=10)
    date = models.DateTimeField()
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
