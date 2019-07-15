from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import View, TemplateResponseMixin


class RetailBillView(TemplateResponseMixin, View):
    template_name = 'billing/retail_bill.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL,
            'range': [1, 5, 10, 15, 20, 25, 30],
            # 'range': ['+1', '+5', '+10', '+15', '+20', '+25', '+30'],
        }
        return self.render_to_response(template_values)
