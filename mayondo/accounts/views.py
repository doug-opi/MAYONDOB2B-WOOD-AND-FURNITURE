from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import AttendantCreationForm
from .models import Profile

# ✅ Custom Login View
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'profile'):
            if user.profile.role == 'manager':
                return reverse_lazy('manager_dashboard')
            elif user.profile.role == 'attendant':
                return reverse_lazy('attendant_dashboard')
        return reverse_lazy('admin:index')  # Default for superuser


# ✅ Logout View
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


# ✅ Manager Dashboard
class ManagerDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'manager_dashboard.html'

    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'manager'


# ✅ Attendant Dashboard
class AttendantDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'attendant_dashboard.html'

    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'attendant'


# ✅ Manager Creates Attendant
class CreateAttendantView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = AttendantCreationForm
    template_name = 'create_attendant.html'
    success_url = reverse_lazy('manager_dashboard')

    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'manager'

    def form_valid(self, form):
        form.save(created_by=self.request.user)
        return super().form_valid(form)


# ✅ Password Reset (for all)
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
