from django.db import models


class Customer(models.Model):
    cat_choices = [('G', 'General'), ('A', 'Category A'), ('B', 'Category B')]

    name = models.CharField(max_length=255, null=True, blank=True)
    firm_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    gstin = models.CharField(max_length=15, null=True, blank=True)
    primary_num = models.BigIntegerField(null=True, blank=True)
    secondary_num = models.BigIntegerField(null=True,blank=True)
    category = models.CharField(max_length=10, choices=cat_choices, default='G')

    def __str__(self):
        return self.name
