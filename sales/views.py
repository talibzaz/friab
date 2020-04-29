import os

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateResponseMixin
from django.template.loader import render_to_string

from django.views import View

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from django.http import JsonResponse
from datetime import date, datetime
import json
import uuid

from .models import Invoice, Item


class ViewCustomerDetails(TemplateResponseMixin, View):
    template_name = 'sales/customer_details.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL
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

        # SAVING INVOICE PDF TO DISK
        path = "sales/pdf/{date}".format(date=today.strftime("%d-%B-%y"))
        html = render_to_string("sales/print-invoice.html", template_data)

        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(path):
            f = open(os.path.join(path, '{name}_{id}.pdf'.format(
                name=self.request.POST['cus_name'].replace(" ", "_"),
                id=invoice_id[0]
            )), 'wb')
            f.write(HTML(string=html, base_url=request.build_absolute_uri()).write_pdf())

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

        prod_obj = []

        for p in products:
            new_item = Item()
            new_item.invoice = invoice
            new_item.item_name = products[p]['product']
            new_item.item_mrp = products[p]['mrp']
            new_item.item_quantity = products[p]['quantity']
            new_item.item_discount = products[p]['discount']
            new_item.item_sp = products[p]['price']
            new_item.item_total = products[p]['total']
            prod_obj.append(new_item)

        Item.objects.bulk_create(prod_obj)

        # WRITING CONTENT TO HTML RESPONSE.
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = "inline; filename=file.pdf"
        font_config = FontConfiguration()
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

        return response


class SearchInvoiceView(TemplateResponseMixin, View):
    template_name = 'sales/search_invoice.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
        }
        return self.render_to_response(template_values)

    def post(self, request):
        criteria = self.request.POST['criteria']

        if criteria == 'id':
            try:
                invoice = Invoice.objects.get(id=self.request.POST['value'])
                data = [{
                    'customer_name': invoice.customer_name,
                    'id': invoice.id,
                    'date': invoice.date.strftime('%d-%B-%y'),
                    'total_amount': invoice.total_amount
                }]
                # data = serializers.serialize('json', invoice)
                return JsonResponse(json.dumps(data), safe=False)
            except Invoice.DoesNotExist:
                return JsonResponse({'error': 'ID does not exist'})
        if criteria == 'name':
            invoice = Invoice.objects.filter(customer_name__icontains=self.request.POST['value']).all()
            if invoice.exists():
                data = []
                for i in invoice.only('customer_name', 'id', 'date', 'total_amount'):
                    data.append({
                        'customer_name': i.customer_name,
                        'id': i.id,
                        'date': i.date.strftime('%d-%B-%y'),
                        'total_amount': i.total_amount
                    })
                return JsonResponse(json.dumps(data), safe=False)
            return JsonResponse({'error': 'Try Again!'})

        if criteria == 'date':
            date_str = self.request.POST['value']
            date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()

            invoice = Invoice.objects.filter(date=date_obj).all()
            if invoice.exists():
                data = []
                for i in invoice.only('customer_name', 'id', 'date', 'total_amount'):
                    data.append({
                        'customer_name': i.customer_name,
                        'id': i.id,
                        'date': i.date.strftime('%d-%B-%y'),
                        'total_amount': i.total_amount
                    })
                return JsonResponse(json.dumps(data), safe=False)
            return JsonResponse({'error': 'Try Again!'})


class UpdateInvoiceView(TemplateResponseMixin, View):
    template_name = 'sales/update_invoice.html'

    def get(self, request, invoice_id):
        invoice = Invoice.objects.get(id=invoice_id)
        items = Item.objects.filter(invoice_id=invoice_id)
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
            'invoice': invoice,
            'items': items,
            'range': [1, 5, 10, 15, 20, 25, 30],
        }
        return self.render_to_response(template_values)

    def post(self, request):

        products = json.loads(self.request.POST['product_list'])

        final_summary = json.loads(self.request.POST['final_summary'])

        invoice_id = self.request.POST['invoice_id']
        inv_date = Invoice.objects.get(id=invoice_id)

        template_data = {
            'customer_name': self.request.POST['cus_name'],
            'customer_address': self.request.POST['cus_address'],
            'customer_phone': self.request.POST['cus_phone'],
            'products': products,
            'final_summary': final_summary,
            'invoice_id': invoice_id,
            'current_date': inv_date.date.strftime("%d-%B-%y"),
        }

        # SAVING DATA TO DB.
        invoice = Invoice.objects.get(id=invoice_id)

        invoice.customer_name = template_data['customer_name']
        invoice.customer_address = template_data['customer_address']
        invoice.customer_phone = template_data['customer_phone']
        invoice.sub_total = template_data['final_summary']['sub_total']
        invoice.last_bal = template_data['final_summary']['last_balance']
        invoice.p_and_f = template_data['final_summary']['p_and_f']
        invoice.round_off = template_data['final_summary']['round_off']
        invoice.total_amount = template_data['final_summary']['total_amount']
        invoice.amount_paid = template_data['final_summary']['amount_paid']
        invoice.current_bal = template_data['final_summary']['current_balance']

        invoice.save()

        for p in products:
            if products[p]['item_id'] != 0:
                i = Item.objects.get(id=products[p]['item_id'])
                i.item_name = products[p]['product']
                i.item_mrp = products[p]['mrp']
                i.item_quantity = products[p]['quantity']
                i.item_discount = products[p]['discount']
                i.item_sp = products[p]['price']
                i.item_total = products[p]['total']
                i.save()
            else:
                i = Item(
                    invoice_id=invoice_id,
                    item_name=products[p]['product'],
                    item_quantity=products[p]['quantity'],
                    item_mrp=products[p]['mrp'],
                    item_discount=products[p]['discount'],
                    item_sp=products[p]['price'],
                    item_total=products[p]['total']
                )
                i.save()

        # WRITING CONTENT TO HTML RESPONSE.
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = "inline; filename=file.pdf"
        html = render_to_string("sales/print-invoice.html", template_data)
        font_config = FontConfiguration()
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

        # SAVING INVOICE PDF TO DISK
        path = "sales/pdf/{date}".format(date=invoice.date.strftime("%d-%B-%y"))
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(path):
            f = open(os.path.join(path, '{name}_{id}.pdf'.format(
                name=self.request.POST['cus_name'].replace(" ", "_"),
                id=invoice_id
            )), 'wb')
            f.write(HTML(string=html, base_url=request.build_absolute_uri()).write_pdf())

        return response


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
            'current_date': date.today(),
            'invoice_id': '12345',
        }
        return self.render_to_response(template_values)
