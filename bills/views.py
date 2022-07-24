from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from products.models import Product
from stores.models import Store
from .forms import (
    InputDetailCreateFormSet,
    OutputDetailCreateFormSet,
    InputDetailUpdateFormSet,
    OutputDetailUpdateFormSet,
)
from .models import Input, Output


class InputsView(LoginRequiredMixin, ListView):
    model = Input
    context_object_name = 'inputs'
    template_name = 'bill/inputs.html'

    def get_queryset(self):
        sk = self.request.GET.get('sk')
        if sk:
            return Input.objects.search(sk).filter(store__user=self.request.user)
        else:
            return Input.objects.filter(store__user=self.request.user)


class InputsDetailView(LoginRequiredMixin, DetailView):
    model = Input
    context_object_name = 'input'
    template_name = 'bill/inputs_detail.html'

    def get_queryset(self):
        return Input.objects.filter(store__user=self.request.user, id=self.kwargs.get('pk'))


class InputsBillView(LoginRequiredMixin, DetailView):
    model = Input
    context_object_name = 'input'
    template_name = 'bill/input_bill.html'

    def get_queryset(self):
        return Input.objects.filter(store__user=self.request.user, id=self.kwargs.get('pk'))


class InputsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Input
    fields = ['store', 'title']
    template_name = 'shared/CreateViewWithInline.html'
    success_url = reverse_lazy('inputs')
    success_message = 'حواله ورود با موفقیت ساخته شد.'

    def get_context_data(self, **kwargs):
        context = super(InputsCreateView, self).get_context_data(**kwargs)
        context['form'].fields['store'].queryset = Store.objects.filter(user=self.request.user)
        if self.request.POST:
            context['details_form'] = InputDetailCreateFormSet(self.request.POST)
        else:
            context['details_form'] = InputDetailCreateFormSet()
            for form in context.get('details_form'):
                form.fields['product'].queryset = Product.objects.filter(user=self.request.user)
        context['name'] = 'حواله ورود'
        context['url'] = reverse('inputs')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        details_form = context['details_form']
        details_form.instance = self.object
        if details_form.is_valid():
            self.object = form.save()
            details_form.instance = self.object
            details_form.save()
            return super(InputsCreateView, self).form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context['details_form'] = details_form
            return self.render_to_response(context)


class InputsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Input
    context_object_name = 'input'
    fields = ['title']
    template_name = 'shared/UpdateViewWithInline.html'
    success_url = reverse_lazy('inputs')
    success_message = 'حواله ورود با موفقیت ویرایش شد.'

    def get_object(self, queryset=None):
        obj = super(InputsUpdateView, self).get_object(queryset)
        if obj.store.user != self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(InputsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['details_form'] = InputDetailUpdateFormSet(self.request.POST, instance=self.object)
        else:
            context['details_form'] = InputDetailUpdateFormSet(instance=self.object)
            for form in context.get('details_form'):
                form.fields['product'].queryset = Product.objects.filter(user=self.request.user)
        context['name'] = 'حواله ورود'
        context['title'] = self.object.title
        context['url'] = reverse('inputs')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        details_form = context['details_form']
        details_form.instance = self.object
        if details_form.is_valid():
            self.object = form.save()
            details_form.instance = self.object
            details_form.save()
            return super(InputsUpdateView, self).form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context['details_form'] = details_form
            return self.render_to_response(context)


class InputsDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Input
    context_object_name = 'input'
    template_name = 'shared/DeleteView.html'
    success_url = reverse_lazy('inputs')
    success_message = 'حواله ورود با موفقیت حذف شد.'

    def get_context_data(self, **kwargs):
        context = super(InputsDeleteView, self).get_context_data(**kwargs)
        context['name'] = 'حواله ورود'
        context['title'] = self.object.title
        context['url'] = reverse('inputs')
        return context

    def get_object(self, queryset=None):
        obj = super(InputsDeleteView, self).get_object(queryset)
        if obj.store.user != self.request.user:
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        try:
            return super(InputsDeleteView, self).post(request, *args, **kwargs)
        except Exception:
            messages.add_message(request, messages.ERROR,
                                 'امکان حذف حواله ورود وجود ندارد.'
                                 ' زیرا توسط حواله خروج یا حواله خروج هایی در حال استفاده است.')
            return HttpResponseRedirect(self.get_success_url())


class OutputsView(LoginRequiredMixin, ListView):
    model = Output
    context_object_name = 'outputs'
    template_name = 'bill/outputs.html'

    def get_queryset(self):
        sk = self.request.GET.get('sk')
        if sk:
            return Output.objects.search(sk).filter(store__user=self.request.user)
        else:
            return Output.objects.filter(store__user=self.request.user)


class OutputsDetailView(LoginRequiredMixin, DetailView):
    model = Output
    context_object_name = 'output'
    template_name = 'bill/outputs_detail.html'

    def get_queryset(self):
        return Output.objects.filter(store__user=self.request.user, id=self.kwargs.get('pk'))


class OutputsBillView(LoginRequiredMixin, DetailView):
    model = Output
    context_object_name = 'output'
    template_name = 'bill/output_bill.html'

    def get_queryset(self):
        return Output.objects.filter(store__user=self.request.user, id=self.kwargs.get('pk'))


class OutputsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Output
    fields = ['store', 'cause']
    template_name = 'shared/CreateViewWithInline.html'
    success_url = reverse_lazy('outputs')
    success_message = 'حواله خروج با موفقیت ساخته شد.'

    def get_context_data(self, **kwargs):
        context = super(OutputsCreateView, self).get_context_data(**kwargs)
        context['form'].fields['store'].queryset = Store.objects.filter(user=self.request.user)
        if self.request.POST:
            context['details_form'] = OutputDetailCreateFormSet(self.request.POST)
        else:
            context['details_form'] = OutputDetailCreateFormSet()
            for form in context.get('details_form'):
                form.fields['product'].queryset = Product.objects.filter(user=self.request.user)
        context['name'] = 'حواله خروج'
        context['url'] = reverse('outputs')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        details_form = context['details_form']
        details_form.instance = self.object
        if details_form.is_valid():
            self.object = form.save()
            details_form.instance = self.object
            details_form.save()
            return super(OutputsCreateView, self).form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context['details_form'] = details_form
            return self.render_to_response(context)


class OutputsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Output
    context_object_name = 'output'
    fields = ['cause']
    template_name = 'shared/UpdateViewWithInline.html'
    success_url = reverse_lazy('outputs')
    success_message = 'حواله خروج با موفقیت ویرایش شد.'

    def get_object(self, queryset=None):
        obj = super(OutputsUpdateView, self).get_object(queryset)
        if obj.store.user != self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(OutputsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['details_form'] = OutputDetailUpdateFormSet(self.request.POST, instance=self.object)
        else:
            context['details_form'] = OutputDetailUpdateFormSet(instance=self.object)
            for form in context.get('details_form'):
                form.fields['product'].queryset = Product.objects.filter(user=self.request.user)
        context['name'] = 'حواله خروج'
        context['title'] = self.object.cause
        context['url'] = reverse('outputs')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        details_form = context['details_form']
        details_form.instance = self.object
        if details_form.is_valid():
            self.object = form.save()
            details_form.instance = self.object
            details_form.save()
            return super(OutputsUpdateView, self).form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context['details_form'] = details_form
            return self.render_to_response(context)


class OutputsDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Output
    context_object_name = 'output'
    template_name = 'shared/DeleteView.html'
    success_url = reverse_lazy('outputs')
    success_message = 'حواله خروج با موفقیت حذف شد.'

    def get_context_data(self, **kwargs):
        context = super(OutputsDeleteView, self).get_context_data(**kwargs)
        context['name'] = 'حواله خروج'
        context['title'] = self.object.cause
        context['url'] = reverse('outputs')
        return context

    def get_object(self, queryset=None):
        obj = super(OutputsDeleteView, self).get_object(queryset)
        if obj.store.user != self.request.user:
            raise Http404
        return obj
