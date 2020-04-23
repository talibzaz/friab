from django.urls import path

from .views import AddNewCustomer

app_name = 'customer'

urlpatterns = [
    path('add-new-customer/', AddNewCustomer.as_view(), name='add-customer'),
]
