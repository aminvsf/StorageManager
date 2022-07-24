from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from stores.models import Store, ProductRecord


class StoresView(LoginRequiredMixin, ListView):
    model = Store
    ordering = ['-created']
    context_object_name = 'stores'
    template_name = 'store/stores.html'

    def get_queryset(self):
        sk = self.request.GET.get('sk')
        if sk:
            return Store.objects.search(sk).filter(user=self.request.user)
        else:
            return Store.objects.filter(user=self.request.user)


class StoresDetailView(LoginRequiredMixin, DetailView):
    model = Store
    context_object_name = 'store'
    template_name = 'store/stores_detail.html'

    def get_queryset(self):
        return Store.objects.filter(user=self.request.user, id=self.kwargs.get('pk'))


class StoresCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Store
    fields = ['name']
    template_name = 'shared/CreateView.html'
    success_url = reverse_lazy('stores')
    success_message = 'انبار با موفقیت ساخته شد.'

    def get_context_data(self, **kwargs):
        context = super(StoresCreateView, self).get_context_data(**kwargs)
        context['name'] = 'انبار'
        context['url'] = reverse('stores')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(StoresCreateView, self).form_valid(form)


class StoresUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Store
    context_object_name = 'store'
    fields = ['name']
    template_name = 'shared/UpdateView.html'
    success_url = reverse_lazy('stores')
    success_message = 'انبار با موفقیت ویرایش شد.'

    def get_context_data(self, **kwargs):
        context = super(StoresUpdateView, self).get_context_data(**kwargs)
        context['name'] = 'انبار'
        context['url'] = reverse('stores')
        return context

    def get_object(self, queryset=None):
        obj = super(StoresUpdateView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj


class StoresDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Store
    context_object_name = 'store'
    template_name = 'shared/DeleteView.html'
    success_url = reverse_lazy('stores')
    success_message = 'انبار با موفقیت حذف شد.'

    def get_context_data(self, **kwargs):
        context = super(StoresDeleteView, self).get_context_data(**kwargs)
        context['name'] = 'محصول'
        context['title'] = self.object.name
        context['url'] = reverse('stores')
        return context

    def get_object(self, queryset=None):
        obj = super(StoresDeleteView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        try:
            return super(StoresDeleteView, self).post(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(request, messages.ERROR,
                                 'امکان حذف انبار وجود ندارد.'
                                 ' زیرا توسط حواله یا حواله هایی در حال استفاده است.')
            return HttpResponseRedirect(self.get_success_url())


class ProductRecordsView(LoginRequiredMixin, ListView):
    model = ProductRecord
    ordering = ['-id']
    context_object_name = 'product_records'
    template_name = 'product_record/product_records.html'

    def get_queryset(self):
        sk = self.request.GET.get('sk')
        if sk:
            return ProductRecord.objects.search(sk).filter(store__user=self.request.user)
        else:
            return ProductRecord.objects.filter(store__user=self.request.user)
