from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin
from django.views import View
from django.http import HttpResponse

from django.conf import settings


class AddNewCustomer(TemplateResponseMixin, View):
    template_name = 'customer/add_new_customer.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
        }
        return self.render_to_response(template_values)

    def post(self, request):
        print(self.request.POST)
        return HttpResponse("Post success!")