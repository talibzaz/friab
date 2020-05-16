from django.urls import path

from .views import CreateInvoiceView, OrderDetailsView, GetCustomerLastBal, \
            TestView, SearchInvoiceView, UpdateInvoiceView, AddRandomBillView

app_name = 'sales'

urlpatterns = [
    path('invoice/', CreateInvoiceView.as_view(), name='invoice'),
    path('search-invoice/', SearchInvoiceView.as_view(), name='search-invoice'),
    path('update-invoice/', UpdateInvoiceView.as_view(), name='update-invoice'),
    path('update-invoice/<str:invoice_id>/', UpdateInvoiceView.as_view(), name='fetch-invoice'),
    path('get-last-bal/<int:customer_id>', GetCustomerLastBal.as_view(), name='last-balance'),
    path('random-bill/', AddRandomBillView.as_view(), name='random-bill'),
    path('test/', TestView.as_view(), name='print-invoice'),
    path('order-info/', OrderDetailsView.as_view(), name='order-info'),
]

