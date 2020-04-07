from django.db import models


class Customer(models.Model):
    cat_choices = [('G', 'General'), ('A', 'Category A'), ('B', 'Category B'), ('C', 'Category C')]

    name = models.CharField(max_length=255, null=False)
    firm_name = models.CharField(max_length=255, null=False)
    address = models.TextField()
    gstin = models.CharField(max_length=15, null=True)
    primary_num = models.IntegerField(null=False)
    secondary_num = models.IntegerField(null=True)
    category = models.CharField(max_length=20, choices=cat_choices)

    def __str__(self):
        return self.name


class Sales(models.Model):
    order_id = models.CharField(max_length=20)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    sub_total = models.FloatField(null=False)
    p_and_f = models.FloatField(null=True)
    round_off = models.FloatField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.FloatField()
    last_bal = models.FloatField()
    current_bal = models.FloatField()
    bill_generated = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id
