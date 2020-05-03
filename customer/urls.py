from django.urls import path

from .views import AddNewCustomer, CustomerList, CustomerDetails, EditCustomerDetailsView

app_name = 'customer'

urlpatterns = [
    path('add-new-customer/', AddNewCustomer.as_view(), name='add-customer'),
    path('list/', CustomerList.as_view(), name='customer-list'),
    path('list/<int:customer_id>/', CustomerDetails.as_view(), name='customer-details'),
    path('list/<int:customer_id>/edit/', EditCustomerDetailsView.as_view(), name='edit-customer')
]
