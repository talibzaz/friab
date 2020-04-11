from django.urls import path

from .views import AddCustomerDetailsView, SaleBillView,\
     OrderDetailsView, ViewCustomerDetails, TestView

app_name = 'sales'

urlpatterns = [
    path('billing/sale-bill/', SaleBillView.as_view(), name='sale-bill'),
    path('test/', TestView.as_view(), name='print-invoice'),
    path('customer/add-customer-details/', AddCustomerDetailsView.as_view(), name='add-cus-details'),
    path('customer/details/', ViewCustomerDetails.as_view(), name='customer-details'),
    path('order-info/', OrderDetailsView.as_view(), name='order-info'),
]

