from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import View, TemplateResponseMixin


class HomeView(TemplateResponseMixin, View):
    template_name = 'app/index.html'

    def get(self, request):
        template_values = {
            'STATIC_URL': settings.STATIC_URL
        }

        return self.render_to_response(template_values)
