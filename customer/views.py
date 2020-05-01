from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin
from django.views import View
from django.http import HttpResponse
from django.conf import settings

from .models import Customer


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
        customers = Customer.objects.all()
        print(customers)
        return self.render_to_response({'STATIC_URL': settings.STATIC_URL, 'customers':customers})