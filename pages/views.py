from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from bills.models import Output


class HomePageView(TemplateView):
    template_name = 'Home.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('panel'))

    def get_context_data(self, **kwargs):
        for output in Output.objects.all():
            output.delete()
        return None
