from django.db import models


class Customer(models.Model):
    cat_choices = [('G', 'General'), ('A', 'Category A'), ('B', 'Category B')]

    name = models.CharField(max_length=255, null=True)
    firm_name = models.CharField(max_length=255, null=True)
    address = models.TextField()
    gstin = models.CharField(max_length=15, null=True)
    primary_num = models.IntegerField(null=True)
    secondary_num = models.IntegerField(null=True)
    category = models.CharField(max_length=20, choices=cat_choices)

    def __str__(self):
        return self.name
