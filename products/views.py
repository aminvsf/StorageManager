from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from products.models import Product, MeasuringUnit


# MeasuringUnits Views

class MeasuringUnitsView(LoginRequiredMixin, ListView):
    model = MeasuringUnit
    context_object_name = 'measuring_units'
    template_name = 'measuring_unit/measuring_units.html'

    def get_queryset(self):
        return MeasuringUnit.objects.filter(user=self.request.user)


class MeasuringUnitsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MeasuringUnit
    fields = ['title']
    template_name = 'shared/CreateView.html'
    success_url = reverse_lazy('measuring-units')
    success_message = 'واحد اندازه گیری با موفقیت ساخته شد.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MeasuringUnitsCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MeasuringUnitsCreateView, self).get_context_data(**kwargs)
        context['name'] = 'واحد اندازه گیری'
        context['url'] = reverse('measuring-units')
        return context


class MeasuringUnitsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MeasuringUnit
    context_object_name = 'measuring_unit'
    fields = ['title']
    template_name = 'shared/UpdateView.html'
    success_url = reverse_lazy('measuring-units')
    success_message = 'واحد اندازه گیری با موفقیت ویرایش شد.'

    def get_context_data(self, **kwargs):
        context = super(MeasuringUnitsUpdateView, self).get_context_data(**kwargs)
        context['name'] = 'واحد اندازه گیری'
        context['title'] = self.object.title
        context['url'] = reverse('measuring-units')
        return context

    def get_object(self, *args, **kwargs):
        obj = super(MeasuringUnitsUpdateView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise Http404
        return obj


class MeasuringUnitsDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = MeasuringUnit
    context_object_name = 'measuring_unit'
    template_name = 'shared/DeleteView.html'
    success_url = reverse_lazy('measuring-units')
    success_message = 'واحد اندازه گیری با موفقیت حذف شد.'

    def get_context_data(self, **kwargs):
        context = super(MeasuringUnitsDeleteView, self).get_context_data(**kwargs)
        context['name'] = 'واحد اندازه گیری'
        context['title'] = self.object.title
        context['url'] = reverse('measuring-units')
        return context

    def get_object(self, queryset=None):
        obj = super(MeasuringUnitsDeleteView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        try:
            return super(MeasuringUnitsDeleteView, self).post(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(request, messages.ERROR,
                                 'امکان حذف واحد اندازه گیری وجود ندارد.'
                                 ' زیرا توسط محصول یا محصول هایی در حال استفاده است.')
            return HttpResponseRedirect(self.get_success_url())


# Products Views

class ProductsView(LoginRequiredMixin, ListView):
    model = Product
    ordering = ['-id']
    context_object_name = 'products'
    template_name = 'product/products.html'

    def get_queryset(self):
        sk = self.request.GET.get('sk')
        if sk:
            return Product.objects.search(sk).filter(user=self.request.user)
        else:
            return Product.objects.filter(user=self.request.user)


class ProductsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    fields = ['title', 'measuring_unit']
    template_name = 'shared/CreateView.html'
    success_url = reverse_lazy('products')
    success_message = 'محصول با موفقیت ساخته شد.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProductsCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductsCreateView, self).get_context_data(**kwargs)
        context['form'].fields['measuring_unit'].queryset = MeasuringUnit.objects.filter(user=self.request.user)
        context['name'] = 'محصول'
        context['url'] = reverse('products')
        return context


class ProductsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    context_object_name = 'product'
    fields = ['title', 'measuring_unit']
    template_name = 'shared/UpdateView.html'
    success_url = reverse_lazy('products')
    success_message = 'محصول با موفقیت ویرایش شد.'

    def get_object(self, queryset=None):
        obj = super(ProductsUpdateView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(ProductsUpdateView, self).get_context_data(**kwargs)
        context['form'].fields['measuring_unit'].queryset = MeasuringUnit.objects.filter(user=self.request.user)
        context['name'] = 'محصول'
        context['title'] = self.object.title
        context['url'] = reverse('products')
        return context


class ProductsDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    template_name = 'shared/DeleteView.html'
    success_url = reverse_lazy('products')
    success_message = 'محصول با موفقیت حذف شد.'

    def get_context_data(self, **kwargs):
        context = super(ProductsDeleteView, self).get_context_data(**kwargs)
        context['name'] = 'محصول'
        context['title'] = self.object.title
        context['url'] = reverse('products')
        return context

    def get_object(self, queryset=None):
        obj = super(ProductsDeleteView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        try:
            return super(ProductsDeleteView, self).post(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(request, messages.ERROR,
                                 'امکان حذف محصول وجود ندارد.'
                                 ' زیرا توسط حواله یا حواله هایی در حال استفاده است.')
            return HttpResponseRedirect(self.get_success_url())
