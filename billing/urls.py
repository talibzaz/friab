from django.urls import path

from .views import RetailBillView

app_name = 'billing'

urlpatterns = [
    path('', RetailBillView.as_view(), name='retail-bill')
]
