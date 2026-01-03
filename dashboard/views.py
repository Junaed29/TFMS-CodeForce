from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import RoleRequiredMixin
from accounts.models import User

class DashboardDispatcher(LoginRequiredMixin, TemplateView):
    """Redirects authenticated users to their specific role dashboard."""
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == User.Role.ADMIN:
            return redirect('dashboard:admin')
        elif user.role == User.Role.HOD:
            return redirect('dashboard:hod')
        elif user.role == User.Role.PSM:
            return redirect('dashboard:psm')
        elif user.role == User.Role.DEAN:
            return redirect('dashboard:dean')
        elif user.role == User.Role.LECTURER:
            return redirect('dashboard:lecturer')
        return redirect('login') # Fallback

class AdminDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/admin_dashboard.html"
    required_role = User.Role.ADMIN

class HODDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/hod_dashboard.html"
    required_role = User.Role.HOD

class PSMDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/psm_dashboard.html"
    required_role = User.Role.PSM

class DeanDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/dean_dashboard.html"
    required_role = User.Role.DEAN

class LecturerDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/lecturer_dashboard.html"
    required_role = User.Role.LECTURER
