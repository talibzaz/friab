from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin
from django.views import View
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Sum
from django.db.models import F

from .models import Customer
from sales.models import Invoice, Item
from helpers.helpers import pg_records
import locale


class AddNewCustomer(TemplateResponseMixin, View):
    template_name = 'customer/add_new_customer.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
        }
        return self.render_to_response(template_values)

    def post(self, request):
        try:
            pri_number = int(self.request.POST['primary_num'])
        except ValueError:
            pri_number = 0
        try:
            sec_number = int(self.request.POST['secondary_num'])
        except ValueError:
            sec_number = 0

        c = Customer(
            name=str(self.request.POST['name']).upper(),
            firm_name=str(self.request.POST['firm_name']).upper(),
            address=str(self.request.POST['address']).upper(),
            gstin=str(self.request.POST['gstin']).upper(),
            primary_num=pri_number,
            secondary_num=sec_number,
            category=self.request.POST['category']
        )
        c.save()

        return render(request, 'customer/add_customer_success.html', {'STATIC_URL': settings.STATIC_URL})


class CustomerList(TemplateResponseMixin, View):
    template_name = 'customer/customer_list.html'

    def get(self, request):
        customers_obj = Customer.objects.order_by("firm_name").all()
        customers = pg_records(request, customers_obj, 10)
        return self.render_to_response({
            'STATIC_URL': settings.STATIC_URL,
            'customers': customers
        })


class CustomerDetails(TemplateResponseMixin, View):
    template_name = 'customer/customer_details.html'

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return render(request, 'app/404.html', {'STATIC_URL': settings.STATIC_URL})
        return self.render_to_response({
            'STATIC_URL': settings.STATIC_URL,
            'customer': customer
        })


class CustomerRecords(TemplateResponseMixin, View):
    template_name = "customer/customer_records.html"

    def get(self, request, customer_id):
        customer = Customer.objects.get(id=customer_id)

        invoice_obj = Invoice.objects.filter(customer_id=customer_id).order_by('-created_at')

        if not invoice_obj:
            invoice = pg_records(request, invoice_obj, 1)
            return self.render_to_response({
                'STATIC_URL': settings.STATIC_URL,
                'invoice': invoice,
                'customer': customer.firm_name,
                'total_sale': 0,
                'current_balance': 0,
                'joined': customer.created_at,
                'visits': 0,
            })

        invoice = pg_records(request, invoice_obj, 10)
        locale.setlocale(locale.LC_MONETARY, 'en_IN')

        total_sale = invoice_obj.exclude(sub_total=0)\
            .aggregate(total=Sum(F('sub_total') + F('p_and_f') + F('round_off')))['total']
        latest_record = invoice_obj.latest('created_at')
        visits = invoice_obj.exclude(sub_total=0).count()

        return self.render_to_response({
            'STATIC_URL': settings.STATIC_URL,
            'invoice': invoice,
            'customer': customer.firm_name,
            'total_sale': locale.currency(total_sale, grouping=True),
            'current_balance': locale.currency(latest_record.current_bal, grouping=True),
            'joined': customer.created_at,
            'visits': visits,
        })


class EditCustomerDetailsView(TemplateResponseMixin, View):
    template_name = "customer/edit_customer.html"

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return render(request, 'app/404.html', {'STATIC_URL': settings.STATIC_URL})
        return self.render_to_response({
            'STATIC_URL': settings.STATIC_URL,
            'customer': customer
        })

    def post(self, request, customer_id):
        try:
            pri_num = int(self.request.POST['primary_num'])
        except ValueError:
            pri_num = 0
        try:
           sec_num = int(self.request.POST['secondary_num'])
        except ValueError:
            sec_num = 0
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.name = str(self.request.POST['name']).upper()
            customer.firm_name = str(self.request.POST['firm_name']).upper()
            customer.address = str(self.request.POST['address']).upper()
            customer.gstin = str(self.request.POST['gstin']).upper()
            customer.primary_num = pri_num
            customer.secondary_num = sec_num
            customer.category = self.request.POST['category']
            customer.save()
        except Customer.DoesNotExist:
            return render(request, 'app/404.html', {'STATIC_URL': settings.STATIC_URL})
        return redirect('customer:customer-details', customer_id)


class RecordView(TemplateResponseMixin, View):
    template_name = "customer/invoice_record.html"

    def get(self, request, invoice_id):
        invoice = Invoice.objects.get(id=invoice_id)

        return self.render_to_response({
            'STATIC_URL': settings.STATIC_URL,
            'invoice': invoice,
            'items': Item.objects.filter(invoice=invoice),
        })
