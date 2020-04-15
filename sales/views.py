import os

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateResponseMixin
from django.template.loader import render_to_string

from django.views import View

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from datetime import date
import json
import uuid

from .models import Invoice, Item


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


class CreateInvoiceView(TemplateResponseMixin, View):
    template_name = 'sales/retail_bill.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
            'range': [1, 5, 10, 15, 20, 25, 30],
        }
        return self.render_to_response(template_values)

    def post(self, request):

        products = json.loads(self.request.POST['product_list'])

        final_summary = json.loads(self.request.POST['final_summary'])

        gen_uuid = uuid.uuid4()
        invoice_id = str(gen_uuid).split("-")

        today = date.today()

        template_data = {
            'customer_name': self.request.POST['cus_name'],
            'customer_address': self.request.POST['cus_address'],
            'customer_phone': self.request.POST['cus_phone'],
            'products': products,
            'final_summary': final_summary,
            'current_date': today.strftime("%d-%B-%y"),
            'invoice_id': invoice_id[0],
        }

        # SAVING DATA TO DB.
        invoice = Invoice(
            id=template_data['invoice_id'],
            customer_name=template_data['customer_name'],
            customer_address=template_data['customer_address'],
            customer_phone=template_data['customer_phone'],
            date=today,
            sub_total=template_data['final_summary']['sub_total'],
            last_bal=template_data['final_summary']['last_balance'],
            p_and_f=template_data['final_summary']['p_and_f'],
            round_off=template_data['final_summary']['round_off'],
            total_amount=template_data['final_summary']['total_amount'],
            amount_paid=template_data['final_summary']['amount_paid'],
            current_bal=template_data['final_summary']['current_balance'],
        )
        invoice.save()

        for p in products:
            item = Item(
                invoice=invoice,
                item_name=products[p]['product'],
                item_quantity=products[p]['quantity'],
                item_mrp=products[p]['mrp'],
                item_discount=products[p]['discount'],
                item_sp=products[p]['price'],
                item_total=products[p]['total'],
            )
            item.save()

        # WRITING CONTENT TO HTML RESPONSE.
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = "inline; filename=file.pdf"
        html = render_to_string("sales/print-invoice.html", template_data)
        font_config = FontConfiguration()
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

        # SAVING INVOICE PDF TO DISK
        path = "sales/pdf/{date}".format(date=today.strftime("%d-%B-%y"))
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(path):
            f = open(os.path.join(path, '{name}_{id}.pdf'.format(
                name=self.request.POST['cus_name'].replace(" ", "_"),
                id=invoice_id[0]
            )), 'wb')
            f.write(HTML(string=html, base_url=request.build_absolute_uri()).write_pdf())

        return response


class SearchInvoiceView(TemplateResponseMixin, View):
    template_name = 'sales/search_invoice.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
        }
        return self.render_to_response(template_values)


class TestView(TemplateResponseMixin, View):
    template_name = 'sales/print-invoice.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
            'customer_name': 'Mohd. Shamim',
            'customer_address': 'Qamarwari',
            'customer_phone': '7006843427',
            'products': '',
            'final_summary': '',
            'current_date': get_current_date(),
            'invoice_id': '12345',
        }
        return self.render_to_response(template_values)


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
