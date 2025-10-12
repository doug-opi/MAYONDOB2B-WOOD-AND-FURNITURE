from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CustomUserCreationForm  # ✅ updated form import
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

# ---------------------------
# LOGIN / LOGOUT
# ---------------------------

class CustomLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        user = self.request.user
        if user.is_superadmin():
            return reverse_lazy('admin:index')
        elif user.is_manager():
            return reverse_lazy('accounts:manager_dashboard')
        elif user.is_attendant():
            return reverse_lazy('accounts:attendant_dashboard')
        return reverse_lazy('accounts:login')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


# ---------------------------
# DASHBOARDS
# ---------------------------

class ManagerDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'manager_dashboard.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_manager()


class AttendantDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'attendant_dashboard.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_attendant()


# ---------------------------
# MANAGER CREATES ATTENDANTS
# ---------------------------

class CreateAttendantView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm  # ✅ use updated form
    template_name = 'create_attendant.html'
    success_url = reverse_lazy('accounts:manager_dashboard')

    def form_valid(self, form):
        # ✅ Automatically assign 'attendant' role when manager creates user
        user = form.save(commit=False)
        user.role = 'attendant'
        user.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_manager()


# ---------------------------
# PASSWORD RESET FLOWS
# ---------------------------

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
