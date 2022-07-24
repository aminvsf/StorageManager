from django.contrib.auth import views
from django.urls import path

from .views import ProfileView

urlpatterns = [
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password-change/', views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
    ),
         name='password-change'),
    path('password-change-done/', views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html',
    ),
         name='password_change_done'),
    path('profile', ProfileView.as_view(), name='profile'),
]
