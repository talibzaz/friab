import os

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateResponseMixin
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.db.models import Q

from django.views import View

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from django.http import JsonResponse
from datetime import datetime
import json

from customer.models import Customer
from .models import Invoice, Item
from sales.utils.utils import save_pdf, generate_unique_id


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
            'customers': Customer.objects.all(),
            'range': [1, 5, 10, 15, 20, 25, 30],
        }
        return self.render_to_response(template_values)

    def post(self, request):
        customer_info = json.loads(self.request.POST['customer_info'])
        c_type = customer_info['type']

        if c_type == 'retail' or c_type == 'create_new':
            customer_name = customer_info['name']
            address = customer_info['address']
            phone = customer_info['phone']
            if c_type == 'create_new':
                customer = self.create_new_customer(customer_info)
        elif c_type == 'existing':
            customer_id = customer_info['customer_id']
            try:
                customer = Customer.objects.get(id=customer_id)
                customer_name = customer.firm_name
                address = customer.address
            except Customer.DoesNotExist:
                customer_name = ''
                address = ''

        products = json.loads(self.request.POST['product_list'])

        final_summary = json.loads(self.request.POST['final_summary'])

        today = datetime.today()
        uniq_id = generate_unique_id()

        template_data = {
            'customer_name': customer_name,
            'customer_address': address,
            'products': products,
            'final_summary': final_summary,
            'current_date': datetime.strptime(final_summary['date'], '%d/%m/%Y').strftime("%d-%B-%y"),
            'invoice_id': uniq_id,
        }

        html = render_to_string("sales/print-invoice.html", template_data)

        # SAVING INVOICE PDF TO TEMP FOLDER SO THAT IF DB QUERY FAILS
        # THE INVOICE PDF WILL STILL BE GENERATED.
        temp_path = "sales/temp_pdf/"
        temp_file = save_pdf(request, html=html, pdf_path=temp_path, today=today, name=customer_name, id=uniq_id)

        # SAVING DATA TO DB.
        if c_type == 'existing' or c_type == 'create_new':
            obj = {
                'name': customer.firm_name,
                'address': customer.address,
                'phone': customer.primary_num
            }
            invoice = self.create_invoice(id=uniq_id, data=final_summary, customer_obj=obj, customer=customer)
        elif c_type == 'retail':
            invoice = self.create_invoice(id=uniq_id, data=final_summary, customer_obj=customer_info, customer=None)

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

        # SAVING INVOICE PDF TO DISK
        sales_path = "sales/pdf/"
        save_pdf(request, html=html, pdf_path=sales_path, today=today, name=customer_name, id=uniq_id)

        # DELETE FILE IN TEMP FOLDER
        os.remove(temp_file)

        if self.request.POST['printing'] == 'save_only':
            return render(request, 'sales/add_invoice_success.html', {
                'STATIC_URL': settings.STATIC_URL
            })

        # WRITING CONTENT TO HTML RESPONSE.
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = "inline; filename=file.pdf"
        font_config = FontConfiguration()
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

        return response

    def create_new_customer(self, customer_info):
        try:
            pri_num = int(customer_info['phone'])
        except ValueError:
            pri_num = 0
        c = Customer.objects.create(
            firm_name=customer_info['name'],
            address=customer_info['address'],
            primary_num= pri_num,
            category='General Category'
        )
        c.save()
        return c

    def create_invoice(self, id, data, customer_obj, customer):
        invoice = Invoice.objects.create(
            id=id,
            customer_name=customer_obj['name'],
            customer=customer,
            customer_address=customer_obj['address'],
            customer_phone=customer_obj['phone'],
            date=datetime.strptime(data['date'], '%d/%m/%Y'),
            sub_total=data['sub_total'],
            last_bal=data['last_balance'],
            p_and_f=data['p_and_f'],
            round_off=data['round_off'],
            total_amount=data['total_amount'],
            amount_paid=data['amount_paid'],
            current_bal=data['current_balance'],
        )
        invoice.save()
        return invoice


class UpdateInvoiceView(TemplateResponseMixin, View):
    template_name = 'sales/update_invoice.html'

    def get(self, request, invoice_id):
        invoice = Invoice.objects.get(id=invoice_id)
        items = Item.objects.filter(invoice_id=invoice_id)
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
            'client': invoice.customer_name,
            'customers': Customer.objects.all(),
            'invoice': invoice,
            'items': items,
            'range': [1, 5, 10, 15, 20, 25, 30],
            'type': 'retail' if invoice.customer is None else 'existing'
        }
        return self.render_to_response(template_values)

    def post(self, request):
        customer_info = json.loads(self.request.POST['customer_info'])
        c_type = customer_info['type']

        if c_type == 'retail' or c_type == 'create_new':
            customer_name = customer_info['name']
            address = customer_info['address']
            phone = customer_info['phone']
            customer = None
            if c_type == 'create_new':
                customer = self.create_new_customer(customer_info)
        elif c_type == 'existing':
            customer_id = customer_info['customer_id']
            try:
                customer = Customer.objects.get(id=customer_id)
                customer_name = customer.firm_name
                address = customer.address
                phone = customer.primary_num
            except Customer.DoesNotExist:
                customer_name = ''
                address = ''

        products = json.loads(self.request.POST['product_list'])

        final_summary = json.loads(self.request.POST['final_summary'])

        invoice_id = self.request.POST['invoice_id']

        invoice = Invoice.objects.get(id=invoice_id)

        template_data = {
            'client': customer_name,
            'customer_name': customer_name,
            'customer_address': address,
            'customer_phone': phone,
            'products': products,
            'final_summary': final_summary,
            'invoice_id': invoice_id,
            # 'current_date': datetime.strptime(final_summary['date'], '%d/%m/%Y').strftime("%d-%B-%y"),
            'current_date': invoice.date.strftime("%d-%B-%y")
        }

        html = render_to_string("sales/print-invoice.html", template_data)

        # SAVING INVOICE PDF TO TEMP FOLDER SO THAT IF DB QUERY FAILS
        # THE INVOICE PDF WILL STILL BE GENERATED.
        temp_path = "sales/temp_pdf/"
        temp_file = save_pdf(request, html=html, pdf_path=temp_path, today=datetime.today(), name=customer_name, id=invoice_id)

        # SAVING DATA TO DB.

        invoice.customer_name = template_data['customer_name']
        invoice.customer = customer
        # invoice.date = datetime.strptime(final_summary['date'], '%d/%m/%Y'),
        invoice.customer_address = template_data['customer_address']
        invoice.customer_phone = template_data['customer_phone']
        invoice.sub_total = final_summary['sub_total']
        invoice.last_bal = final_summary['last_balance']
        invoice.p_and_f = final_summary['p_and_f']
        invoice.round_off = final_summary['round_off']
        invoice.total_amount = final_summary['total_amount']
        invoice.amount_paid = final_summary['amount_paid']
        invoice.current_bal = final_summary['current_balance']

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
        font_config = FontConfiguration()
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

        # SAVING INVOICE PDF TO DISK
        sales_path = "sales/pdf/"
        save_pdf(request, html=html, pdf_path=sales_path, today=invoice.date, name=customer_name, id=invoice_id)

        # DELETE FILE IN TEMP FOLDER
        os.remove(temp_file)

        if self.request.POST['printing'] == 'save_only':
            return redirect('customer:record-view', invoice_id=invoice_id)

        # WRITING CONTENT TO HTML RESPONSE.
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = "inline; filename=file.pdf"
        font_config = FontConfiguration()
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

        return response

    def create_new_customer(self, customer_info):
        try:
            pri_num = int(customer_info['phone'])
        except ValueError:
            pri_num = 0
        c = Customer.objects.create(
            firm_name=customer_info['name'],
            address=customer_info['address'],
            primary_num= pri_num,
            category='General Category'
        )
        c.save()
        return c


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
                    'total_amount': invoice.total_amount,
                    'current_bal': invoice.current_bal,
                    'amount_paid': invoice.amount_paid
                }]
                # data = serializers.serialize('json', invoice)
                return JsonResponse(json.dumps(data), safe=False)
            except Invoice.DoesNotExist:
                return JsonResponse({'error': 'ID does not exist'})
        if criteria == 'name':
            invoice = Invoice.objects.filter(Q(customer_name__icontains=self.request.POST['value']) | Q(customer__name__icontains=self.request.POST['value'])).all().order_by('-created_at')
            if invoice.exists():
                data = []
                for i in invoice.only('customer_name', 'id', 'date', 'total_amount'):
                    data.append({
                        'customer_name': i.customer_name,
                        'id': i.id,
                        'date': i.date.strftime('%d-%B-%y'),
                        'total_amount': i.total_amount,
                        'current_bal': i.current_bal,
                        'amount_paid': i.amount_paid
                    })
                return JsonResponse(json.dumps(data), safe=False)
            return JsonResponse({'error': 'Try Again!'})

        if criteria == 'date':
            date_str = self.request.POST['value']
            date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()

            invoice = Invoice.objects.filter(date=date_obj).all().order_by('customer_name')
            if invoice.exists():
                data = []
                for i in invoice.only('customer_name', 'id', 'date', 'total_amount'):
                    data.append({
                        'customer_name': i.customer_name,
                        'id': i.id,
                        'date': i.date.strftime('%d-%B-%y'),
                        'total_amount': i.total_amount,
                        'current_bal': i.current_bal,
                        'amount_paid': i.amount_paid
                    })
                return JsonResponse(json.dumps(data), safe=False)
            return JsonResponse({'error': 'Try Again!'})


class GetCustomerLastBal(View):
    def get(self, request, customer_id):
        customer = Customer.objects.get(id=customer_id)
        try:
            invoice = Invoice.objects.filter(customer=customer).latest('created_at')
        except Invoice.DoesNotExist:
            return JsonResponse({'current_bal': 0})
        return JsonResponse({'current_bal': invoice.current_bal}, safe=False)


class AddRandomBillView(TemplateResponseMixin, View):
    template_name = 'sales/add_random_bill.html'

    def get(self, request):
        return self.render_to_response({
            'STATIC_URL': settings.STATIC_URL,
            'customers': Customer.objects.all()
        })

    def post(self, request):
        try:
            customer = Customer.objects.get(id=self.request.POST['customer_id'])
            amount_paid = self.request.POST['amount_paid']
            total_amount = self.request.POST['total_amount']
            Invoice(
                id=generate_unique_id(),
                customer_name=customer.firm_name,
                customer=customer,
                customer_address=customer.address,
                customer_phone=customer.primary_num,
                date=datetime.strptime(self.request.POST['date'], '%d/%m/%Y'),
                sub_total=self.request.POST['sub_total'],
                last_bal=self.request.POST['last_balance'],
                p_and_f=self.request.POST['p_and_f'],
                amount_paid=amount_paid,
                total_amount=total_amount,
                current_bal=int(total_amount) - int(amount_paid)
            ).save()

        except Customer.DoesNotExist:
            return render(request, 'app/404.html', {
                'STATIC_URL': settings.STATIC_URL
            })
        return render(request, 'sales/add_random_bill_success.html', {
            'STATIC_URL': settings.STATIC_URL
        })


def DeleteInvoiceItem(request):
    invoice_inst = Invoice.objects.get(id=request.POST['invoice_id'])
    invoice_inst.sub_total = request.POST['sub_total']
    invoice_inst.total_amount = request.POST['total_amount']
    invoice_inst.current_bal = request.POST['current_balance']
    invoice_inst.save()
    item_inst = Item.objects.filter(Q(invoice__id=request.POST['invoice_id']) & Q(id=request.POST['item_id']))
    item_inst.delete()
    return JsonResponse({'data': 'ok'}, status=200)


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
