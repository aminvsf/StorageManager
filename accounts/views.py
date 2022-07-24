from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

User = get_user_model()


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    success_url = reverse_lazy('profile')
    success_message = 'اطلاعات کاربری با موفقیت ویرایش شد.'
    template_name = 'account/profile.html'

    def get_object(self, queryset=None):
        return self.request.user
