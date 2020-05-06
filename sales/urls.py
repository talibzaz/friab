from django.urls import path

from .views import CreateInvoiceView, OrderDetailsView, \
            TestView, SearchInvoiceView, UpdateInvoiceView

app_name = 'sales'

urlpatterns = [
    path('invoice/', CreateInvoiceView.as_view(), name='invoice'),
    path('search-invoice/', SearchInvoiceView.as_view(), name='search-invoice'),
    path('update-invoice/', UpdateInvoiceView.as_view(), name='update-invoice'),
    path('update-invoice/<str:invoice_id>/', UpdateInvoiceView.as_view(), name='fetch-invoice'),
    path('test/', TestView.as_view(), name='print-invoice'),
    path('order-info/', OrderDetailsView.as_view(), name='order-info'),
]

