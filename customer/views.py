from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin
from django.views import View
from django.conf import settings

from .models import Customer
from helpers.helpers import pg_records


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
            gstin=self.request.POST['gstin'],
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


class EditCustomerDetailsView(TemplateResponseMixin, View):
    template_name = "customer/edit_customer.html"

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return request(request, 'app/404.html', {'STATIC_URL': settings.STATIC_URL})
        return self.render_to_response({
            'STATIC_URL': settings.STATIC_URL,
            'customer': customer
        })
