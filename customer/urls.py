from django.urls import path

from .views import AddNewCustomer, CustomerList

app_name = 'customer'

urlpatterns = [
    path('add-new-customer/', AddNewCustomer.as_view(), name='add-customer'),
    path('list/', CustomerList.as_view(), name='customer-list')
]
