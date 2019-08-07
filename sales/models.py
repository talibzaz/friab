from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255, null=False)
    firm_name = models.CharField(max_length=255, null=False)
    address = models.TextField()
    gstin = models.CharField(max_length=15, null=True)
    primary_num = models.IntegerField(null=False)
    secondary_num = models.IntegerField(null=True)
    category = models.CharField(max_length=20, choices=[('A', 'Category A'), ('B', 'Category B'), ('C', 'Category C')])

    def __str__(self):
        return self.name


class Sales(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    sub_total = models.IntegerField(null=False)
    shipping_charges = models.IntegerField(null=True)
    date = models.DateTimeField()
    amount_paid = models.IntegerField()
    remaining_bal = models.IntegerField()

    def __str__(self):
        return self.customer_id, self.amount_paid
