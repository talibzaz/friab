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
    invoice_id = models.CharField(max_length=120)
    customer_name = models.CharField(max_length=20, default='CASH')
    customer_address = models.CharField(max_length=30, blank=True)
    customer_phone = models.CharField(blank=True, max_length=10)
    sub_total = models.FloatField(null=False)
    p_and_f = models.FloatField(default=0)
    round_off = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.IntegerField(default=0)
    last_bal = models.IntegerField(default=0)
    current_bal = models.IntegerField(default=0)

    def __str__(self):
        return self.invoice_id
