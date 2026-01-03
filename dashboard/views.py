from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .mixins import RoleRequiredMixin
from accounts.models import User
from university.models import TaskForce, Department
from .forms import StaffForm, TaskForceForm, DepartmentForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_count'] = User.objects.exclude(role=User.Role.ADMIN).count()
        context['taskforce_count'] = TaskForce.objects.count()
        context['department_count'] = Department.objects.count()
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        return context

# --- Admin Department Management ---
class DepartmentListView(RoleRequiredMixin, ListView):
    model = Department
    template_name = "dashboard/admin/department_list.html"
    context_object_name = "departments"
    required_role = User.Role.ADMIN

class DepartmentCreateView(RoleRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "dashboard/admin/department_form.html"
    success_url = reverse_lazy('dashboard:department_list')
    required_role = User.Role.ADMIN

# --- Admin Staff Management ---
class StaffListView(RoleRequiredMixin, ListView):
    model = User
    template_name = "dashboard/admin/staff_list.html"
    context_object_name = "staff_list"
    required_role = User.Role.ADMIN
    
    def get_queryset(self):
         return User.objects.all().order_by('-date_joined')

class StaffCreateView(RoleRequiredMixin, CreateView):
    model = User
    form_class = StaffForm
    template_name = "dashboard/admin/staff_form.html"
    success_url = reverse_lazy('dashboard:staff_list')
    required_role = User.Role.ADMIN

# --- Admin Task Force Management ---
class TaskForceListView(RoleRequiredMixin, ListView):
    model = TaskForce
    template_name = "dashboard/admin/taskforce_list.html"
    context_object_name = "taskforces"
    required_role = User.Role.ADMIN

class TaskForceCreateView(RoleRequiredMixin, CreateView):
    model = TaskForce
    form_class = TaskForceForm
    template_name = "dashboard/admin/taskforce_form.html"
    success_url = reverse_lazy('dashboard:taskforce_list')
    required_role = User.Role.ADMIN

class HODDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/hod_dashboard.html"
    required_role = User.Role.HOD

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.department:
            context['taskforce_count'] = TaskForce.objects.filter(departments=self.request.user.department).count()
        else:
            context['taskforce_count'] = 0
        return context

from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import (
    StaffForm, TaskForceForm, DepartmentForm, TaskForceMembershipForm
)

# ... (Previous imports)

class HODTaskForceListView(RoleRequiredMixin, ListView):
    model = TaskForce
    template_name = "dashboard/hod/taskforce_list.html"
    context_object_name = "taskforces"
    required_role = User.Role.HOD

    def get_queryset(self):
        # Filter task forces that include the HOD's department
        if not self.request.user.department:
            return TaskForce.objects.none()
        return TaskForce.objects.filter(departments=self.request.user.department).distinct()

class HODTaskForceUpdateView(RoleRequiredMixin, UpdateView):
    model = TaskForce
    form_class = TaskForceMembershipForm
    template_name = "dashboard/hod/taskforce_manage.html"
    context_object_name = "taskforce"
    required_role = User.Role.HOD
    success_url = reverse_lazy('dashboard:hod_taskforce_list')

    def get_queryset(self):
        # Ensure HOD can only edit task forces for their department
        if not self.request.user.department:
            return TaskForce.objects.none()
        return TaskForce.objects.filter(departments=self.request.user.department)

    def get_form_kwargs(self):
        """Pass the HOD's department to the form to filter staff."""
        kwargs = super().get_form_kwargs()
        kwargs['department'] = self.request.user.department
        return kwargs

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'submit':
            form.instance.status = 'SUBMITTED'
        # If action is 'save', status remains as is (likely ACTIVE or REJECTED)
        return super().form_valid(form)

class PSMDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/psm_dashboard.html"
    required_role = User.Role.PSM
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Count Pending Approvals
        context['pending_count'] = TaskForce.objects.filter(status='SUBMITTED').count()
        return context

class PSMTaskForceListView(RoleRequiredMixin, ListView):
    model = TaskForce
    template_name = "dashboard/psm/taskforce_list.html"
    context_object_name = "taskforces"
    required_role = User.Role.PSM

    def get_queryset(self):
        # PSM sees SUBMITTED task forces for approval
        return TaskForce.objects.filter(status='SUBMITTED').order_by('-updated_at')

from django.views.generic import DetailView

class PSMTaskForceDetailView(RoleRequiredMixin, DetailView):
    model = TaskForce
    template_name = "dashboard/psm/taskforce_review.html"
    context_object_name = "taskforce"
    required_role = User.Role.PSM
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action = request.POST.get('action')
        
        if action == 'approve':
            self.object.status = 'APPROVED'
            self.object.save()
            return redirect('dashboard:psm_taskforce_list')
            
        elif action == 'reject':
            reason = request.POST.get('rejection_reason')
            if reason:
                self.object.rejection_reason = reason
                self.object.status = 'REJECTED'
                self.object.save()
                return redirect('dashboard:psm_taskforce_list')
            else:
                 # Should handle error (empty reason), but keeping simple for now
                 pass
                 
        return redirect('dashboard:psm_taskforce_list')

class DeanDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/dean_dashboard.html"
    required_role = User.Role.DEAN

class LecturerDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/lecturer_dashboard.html"
    required_role = User.Role.LECTURER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Count assignments
        context['assignment_count'] = TaskForce.objects.filter(members=self.request.user, status='APPROVED').count()
        return context

class LecturerTaskForceListView(RoleRequiredMixin, ListView):
    model = TaskForce
    template_name = "dashboard/lecturer/portfolio.html"
    context_object_name = "taskforces"
    required_role = User.Role.LECTURER

    def get_queryset(self):
        # Lecturer sees Task Forces they are a member of OR chairman of
        # Filter by APPROVED only? SRS doesn't specify, but usually they work on Approved ones.
        # Let's show all for visibility, maybe filter stats in template.
        from django.db.models import Q
        return TaskForce.objects.filter(
            Q(members=self.request.user) | Q(chairman=self.request.user)
        ).distinct().order_by('-updated_at')
