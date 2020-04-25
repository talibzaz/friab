from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin
from django.views import View
from django.http import HttpResponse
from django.conf import settings

from .models import Customer
from .forms.forms import CustomerProfile


class AddNewCustomer(TemplateResponseMixin, View):
    template_name = 'customer/add_new_customer.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
        }
        return self.render_to_response(template_values)

    def post(self, request):
        print(self.request.POST['category'])
        # form = CustomerProfile(self.request.POST)
        # if form.is_valid():
        #     print('here')
        #     customer = form.save()
        Customer(
            name=str(self.request.POST['name']).upper(),
            firm_name=str(self.request.POST['firm_name']).upper(),
            address=str(self.request.POST['address']).upper(),
            gstin=self.request.POST['gstin'],
            primary_num=self.request.POST['primary_num'],
            secondary_num=self.request.POST['secondary_num'],
            category=self.request.POST['category']
        ).save()

        return HttpResponse("Post success!")