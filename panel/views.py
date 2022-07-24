from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from bills.models import Input, Output
from bills.utils import date_filters


class PanelView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/panel.html'

    def get_context_data(self, **kwargs):
        context = super(PanelView, self).get_context_data(**kwargs)
        exact_datetime = datetime.now().astimezone()
        # Input bills
        inputs_result = date_filters(exact_datetime, Input, self.request.user)
        context['inputs_monthly'], context['inputs_weekly'], context['inputs_yesterday'], context[
            'inputs_today'] = inputs_result
        # Output bills
        outputs_result = date_filters(exact_datetime, Output, self.request.user)
        context['outputs_monthly'], context['outputs_weekly'], context['outputs_yesterday'], context[
            'outputs_today'] = outputs_result
        return context
