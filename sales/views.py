from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from django.views.generic.base import View, TemplateResponseMixin

import json


class AddCustomerDetailsView(TemplateResponseMixin, View):
    template_name = 'sales/add-customer-details.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
        }
        return self.render_to_response(template_values)

    def post(self, request):
        print(self.request.POST)
        return HttpResponse("Post success!")


class ViewCustomerDetails(TemplateResponseMixin, View):
    template_name = 'sales/customer_details.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL
        }
        return self.render_to_response(template_values)


class SaleBillView(TemplateResponseMixin, View):
    template_name = 'sales/retail_bill.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
            'range': [1, 5, 10, 15, 20, 25, 30],
        }
        return self.render_to_response(template_values)

    def post(self, request):
        print(self.request.POST)
        products = json.loads(self.request.POST['product_list'])
        for key in products:
            print(products[key])

        final_summary = json.loads(self.request.POST['final_summary'])
        print(final_summary['round_off'])

        return HttpResponse('POSTED!')


class TestView(View):
    # Get list of customers
    def get(self, request):
        return HttpResponse('List containing customers')


class PrintInvoiceView(TemplateResponseMixin, View):
    template_name = 'sales/print-invoice.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
            'customer_name': 'John Doe',
            'customer_address': 'Magam, Baramulla',
            'customer_phone': '+91 990 669 6262',
            'order_id': 'C12J91',

        }
        return self.render_to_response(template_values)


class GetCustomersList(View):
    # Get list of customers
    def get(self, request):
        return HttpResponse('List containing customers')


class OrderDetailsView(TemplateResponseMixin, View):
    template_name = 'sales/order_info.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
        }
        if 'order_id' in self.request.GET:
            self.template_name = 'sales/order_info_by_id.html'
            template_values.update({
                'warning_class': 'hidden',
                'info_class': 'active',
            })
            # TODO find order by the given order id and return the view......
        return self.render_to_response(template_values)
