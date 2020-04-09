from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateResponseMixin
from django.template.loader import render_to_string

from django.views import View

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

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

        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = "inline; filename=file.pdf"
        html = render_to_string("sales/print-invoice.html", {
            'customer_name': self.request.POST['cus_name'],
            'customer_address': self.request.POST['cus_address'],
            'customer_phone': self.request.POST['cus_phone'],
            'products': products,
            'final_summary': final_summary
        })
        font_config = FontConfiguration()
        HTML(string=html).write_pdf(response, font_config=font_config)
        return response


# class PrintInvoiceView(View):
#
#     def get(self, request):
#         template_values = {
#             'STATIC_URL': settings.STATIC_URL,
#             'customer_name': 'John Doe',
#             'customer_address': 'Magam, Baramulla',
#             'customer_phone': '+91 990 669 6262',
#             'order_id': 'C12J91',
#
#         }
#         response = HttpResponse(content_type="application/pdf")
#         response['Content-Disposition'] = "inline; filename=file.pdf"
#         html = render_to_string("sales/print-invoice.html", {
#             'STATIC_URL': settings.STATIC_URL,
#             'customer_name': 'John Doe',
#             'customer_address': 'Magam, Baramulla',
#             'customer_phone': '+91 990 669 6262',
#             'order_id': 'C12J91',
#         })
#         font_config = FontConfiguration()
#         HTML(string=html).write_pdf(response, font_config=font_config)
#         return response


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
