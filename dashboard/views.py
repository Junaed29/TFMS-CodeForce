from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .mixins import RoleRequiredMixin
from accounts.models import User, AuditLog
from university.models import TaskForce, Department, WorkloadSettings
from .forms import StaffForm, TaskForceForm, DepartmentForm, WorkloadSettingsForm

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
        context['recent_logs'] = AuditLog.objects.select_related('actor').order_by('-timestamp')[:5]
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

class DepartmentUpdateView(RoleRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = "dashboard/admin/department_form.html"
    success_url = reverse_lazy('dashboard:department_list')
    required_role = User.Role.ADMIN

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

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

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        
        # Generate Temp Password
        temp_password = get_random_string(10)
        user.set_password(temp_password)
        user.must_change_password = True
        user.save()
        
        # Send Email
        # Send Email
        subject = "Welcome to Task Force Management System"
        context = {
            'user': user,
            'temp_password': temp_password,
            'login_url': self.request.build_absolute_uri(reverse_lazy('login'))
        }
        html_message = render_to_string('email/account_created.html', context)
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)
            messages.success(self.request, f"Staff created. Email sent to {user.email}.")
        except Exception as e:
            print(f"Error sending email: {e}")
            messages.warning(self.request, f"Staff created, but email failed to send. Temp Password: {temp_password}")

        log_action(self.request, self.request.user, "CREATE_USER", "User", user.pk, f"Created user {user.username}")
        
        return response

class StaffUpdateView(RoleRequiredMixin, UpdateView):
    model = User
    form_class = StaffForm
    template_name = "dashboard/admin/staff_form.html"
    success_url = reverse_lazy('dashboard:staff_list')
    required_role = User.Role.ADMIN
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

class StaffPasswordResetView(RoleRequiredMixin, View):
    required_role = User.Role.ADMIN

    def post(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
            
            # Use PasswordResetForm to send the standard reset link
            form = PasswordResetForm({'email': user.email})
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                    email_template_name='registration/password_reset_email.html',
                    html_email_template_name='registration/password_reset_email.html',
                    subject_template_name='registration/password_reset_subject.txt'
                )
                messages.success(request, f"Password reset link sent to {user.email}.")
                log_action(request, request.user, "RESET_PASSWORD", "User", user.pk, f"Sent password reset link for {user.username}")
            else:
                 messages.error(request, f"Could not send reset link. Invalid email for user {user.username}?")

        except User.DoesNotExist:
            messages.error(request, "User not found.")
            
        return redirect('dashboard:staff_edit', pk=pk)

class StaffUnlockView(RoleRequiredMixin, View):
    required_role = User.Role.ADMIN

    def post(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
            user.is_locked = False
            user.failed_attempts = 0
            user.save()
            
            
            # Send Email
            # Send Email
            subject = "Account Unlocked - Task Force Management System"
            context = {
                'headline': "Account Unlocked",
                'body_text': f"Hello {user.get_full_name()},\n\nYour account has been unlocked. You can now log in to the system.",
                'action_url': request.build_absolute_uri(reverse_lazy('login')),
                'action_text': "Login Now"
            }
            html_message = render_to_string('email/notification.html', context)
            plain_message = strip_tags(html_message)

            try:
                send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)
            except Exception as e:
                print(f"Error sending email: {e}")

            messages.success(request, f"Account unlocked for {user.username}. Email sent.")
            log_action(request, request.user, "UNLOCK_USER", "User", user.pk, f"Unlocked user {user.username}")
            
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            
        return redirect('dashboard:staff_list')

class StaffDeactivateView(RoleRequiredMixin, View):
    required_role = User.Role.ADMIN

    def post(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
            justification = request.POST.get('justification')
            if not justification:
                messages.error(request, "Justification is required to deactivate a user.")
                return redirect(request.META.get('HTTP_REFERER', 'dashboard:staff_list'))

            user.is_active = False
            user.save()
            
            
            # Send Email
            # Send Email
            subject = "Account Deactivated - Task Force Management System"
            context = {
                'headline': "Account Deactivated",
                'body_text': f"Hello {user.get_full_name()},\n\nYour account has been deactivated.\n\nReason: {justification}\n\nPlease contact IT support if you believe this is an error.",
            }
            html_message = render_to_string('email/notification.html', context)
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)
            except Exception as e:
                print(f"Error sending email: {e}")

            messages.success(request, f"User {user.username} deactivated successfully. Notification email sent.")
            log_action(request, request.user, "DEACTIVATE_USER", "User", user.pk, f"Deactivated user {user.username}. Reason: {justification}")
            
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            
        return redirect('dashboard:staff_list')

class StaffActivateView(RoleRequiredMixin, View):
    required_role = User.Role.ADMIN

    def post(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = True
            user.is_locked = False # Also unlock if they were locked
            user.failed_attempts = 0
            user.save()
            
            
            # Send Email
            # Send Email
            subject = "Account Activated - Task Force Management System"
            context = {
                'headline': "Account Reactivated",
                'body_text': f"Hello {user.get_full_name()},\n\nYour account has been reactivated. You can now log in.",
                'action_url': request.build_absolute_uri(reverse_lazy('login')),
                'action_text': "Login Now"
            }
            html_message = render_to_string('email/notification.html', context)
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)
            except Exception as e:
                print(f"Error sending email: {e}")

            messages.success(request, f"User {user.username} activated successfully. Notification email sent.")
            log_action(request, request.user, "ACTIVATE_USER", "User", user.pk, f"Activated user {user.username}")
            
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            
        return redirect('dashboard:staff_list')

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

class TaskForceUpdateView(RoleRequiredMixin, UpdateView):
    model = TaskForce
    form_class = TaskForceForm
    template_name = "dashboard/admin/taskforce_form.html"
    success_url = reverse_lazy('dashboard:taskforce_list')
    required_role = User.Role.ADMIN
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit Task Force"
        return context

class WorkloadSettingsView(RoleRequiredMixin, UpdateView):
    model = WorkloadSettings
    form_class = WorkloadSettingsForm
    template_name = "dashboard/admin/workload_settings.html"
    success_url = reverse_lazy('dashboard:admin')
    required_role = User.Role.ADMIN

    def get_object(self, queryset=None):
        # Singleton pattern: ensure one exists
        obj, created = WorkloadSettings.objects.get_or_create(pk=1)
        return obj

    def form_valid(self, form):
        messages.success(self.request, "Workload thresholds updated successfully.")
        log_action(self.request, self.request.user, "UPDATE_SETTINGS", "WorkloadSettings", self.object.pk, f"Updated thresholds: Min={form.instance.min_weightage}, Max={form.instance.max_weightage}")
        return super().form_valid(form)

class HODDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/hod_dashboard.html"
    required_role = User.Role.HOD

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.department:
            taskforces = TaskForce.objects.filter(departments=self.request.user.department).distinct()
            context['taskforce_count'] = taskforces.count()
            context['taskforces'] = taskforces
        else:
            context['taskforce_count'] = 0
            context['taskforces'] = TaskForce.objects.none()
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
    locked_statuses = {'APPROVED', 'SUBMITTED', 'INACTIVE'}

    def get_queryset(self):
        # Ensure HOD can only edit task forces for their department
        if not self.request.user.department:
            return TaskForce.objects.none()
        return TaskForce.objects.filter(departments=self.request.user.department)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status in self.locked_statuses:
            messages.error(request, "This task force is locked while submitted, approved, or inactive.")
            return redirect('dashboard:hod_taskforce_list')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Pass the HOD's department to the form to filter staff."""
        kwargs = super().get_form_kwargs()
        kwargs['department'] = self.request.user.department
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from university.services import WorkloadService
        import json
        
        # Serialize Members
        members_data = []
        for member in self.object.members.all():
            # Calculate workload (including this task force as they are already a member)
            status = WorkloadService.get_workload_status(member)
            members_data.append({
                'id': member.id,
                'name': member.get_full_name() or member.username,
                'email': member.email,
                'role': member.get_role_display(),
                'workload': status
            })
        
        context['current_members_json'] = json.dumps(members_data)
        return context

    def form_valid(self, form):
        action = self.request.POST.get('action')
        
        # Check if justification is needed but missing
        # (This is a fallback; frontend should catch this, but backend must enforce)
        # However, checking overload here is complex without re-calculating everything.
        # Let's rely on the fact that if they click 'Submit', they are claiming it's ready.
        # Ideally, we should check overload status here.
        
        if action == 'submit':
            form.instance.status = 'SUBMITTED'
            # Check for justification if provided
            justification = self.request.POST.get('justification')
            if justification:
                # Append to description or save to a new field if we had one.
                # Use Case says "Prompt Justification". 
                # Let's append to description for now as 'Justification: ...'
                # Or usage rejection_reason? No, that's for PSM.
                # Let's append to description.
                current_desc = form.instance.description or ""
                form.instance.description = f"{current_desc}\n\n[Justification]: {justification}".strip()

            response = super().form_valid(form)
            log_action(self.request, self.request.user, "SUBMIT_TASKFORCE", "TaskForce", self.object.pk, "Submitted for approval")
            
            # Send Email logic (kept same)
            subject = f"Task Force Submitted: {self.object.name}"
            context = {
                'headline': "Submission Successful",
                'body_text': f"Hello {self.request.user.get_full_name()},\n\nYou have successfully submitted the Task Force '{self.object.name}' for approval.",
                'action_url': self.request.build_absolute_uri(reverse_lazy('dashboard:hod_taskforce_list')),
                'action_text': "View Status"
            }
            html_message = render_to_string('email/notification.html', context)
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [self.request.user.email], html_message=html_message)
            except Exception as e:
                print(f"Error sending email: {e}")
                
            messages.success(self.request, f"Task Force '{self.object.name}' submitted successfully. Confirmation email sent.")
            return response
            
        elif action == 'save_draft':
            # Save as DRAFT if it was Draft or Active.
            # If it was Active (from creation), keeping it Active is fine, or switching to Draft?
            # User workflow: "Save Draft". Implies switching to DRAFT status if not already.
            # But if it was ACTIVE, maybe we shouldn't demote it?
            # Actually, `DRAFT` is a new status. Let's use it.
            if form.instance.status != 'ACTIVE': # Don't change Active to Draft if it was already live?
                 form.instance.status = 'DRAFT'
            else:
                 # If it was defined as ACTIVE by default logic, maybe we want to keep it active?
                 # Typically 'Save Draft' means "Work in Progress".
                 pass 
            
            # For this specific request: "system will not save that data... until clicking the review request"
            # But we added "Save Draft". 
            # Let's set it to DRAFT.
            form.instance.status = 'DRAFT'
            response = super().form_valid(form)
            messages.success(self.request, "Draft saved successfully.")
            return response

        return super().form_valid(form)

from accounts.utils import log_action
import csv
from django.http import HttpResponse

class AuditLogListView(RoleRequiredMixin, ListView):
    model = AuditLog
    template_name = "dashboard/admin/audit_log.html"
    context_object_name = "logs"
    required_role = User.Role.ADMIN
    paginate_by = 20

    def get_queryset(self):
        queryset = AuditLog.objects.all().select_related('actor')
        user_query = self.request.GET.get('user')
        if user_query:
            queryset = queryset.filter(actor__username__icontains=user_query)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        # Handle Export
        if self.request.GET.get('export') == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="audit_logs.csv"'
            writer = csv.writer(response)
            writer.writerow(['Timestamp', 'Actor', 'Action', 'Target Model', 'Target ID', 'Details', 'IP'])
            for log in self.get_queryset():
                writer.writerow([log.timestamp, log.actor, log.action, log.target_model, log.target_id, log.details, log.ip_address])
            return response
        return super().render_to_response(context, **response_kwargs)

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
            log_action(request, request.user, "APPROVE_TASKFORCE", "TaskForce", self.object.pk, f"Approved task force: {self.object.name}")
            
            # Send Email logic (removed chairman specific email)
            # Consider emailing HODs of involved departments instead?
            # For now, no individual email if no specific leader.
            pass

            messages.success(request, f"Task Force '{self.object.name}' approved.")
            return redirect('dashboard:psm_taskforce_list')
            
        elif action == 'reject':
            reason = request.POST.get('rejection_reason')
            if reason:
                self.object.rejection_reason = reason
                self.object.status = 'REJECTED'
                self.object.save()
                log_action(request, request.user, "REJECT_TASKFORCE", "TaskForce", self.object.pk, f"Rejected with reason: {reason}")
                
                # Send Email logic (removed chairman specific email)
                # Consider emailing HODs of involved departments instead?
                pass

                messages.success(request, f"Task Force '{self.object.name}' rejected.")
                return redirect('dashboard:psm_taskforce_list')
            else:
                 pass
                 
        return redirect('dashboard:psm_taskforce_list')

class DeanDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/dean_dashboard.html"
    required_role = User.Role.DEAN
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Executive Stats
        context['total_taskforces'] = TaskForce.objects.count()
        context['active_taskforces'] = TaskForce.objects.filter(status='APPROVED').count()
        context['pending_approvals'] = TaskForce.objects.filter(status='SUBMITTED').count()
        return context

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
            Q(members=self.request.user)
        ).distinct().order_by('-updated_at')

class DeanReportView(RoleRequiredMixin, ListView):
    model = TaskForce
    template_name = "dashboard/dean/report_list.html"
    context_object_name = "taskforces"
    required_role = User.Role.DEAN

    def get_queryset(self):
        # Dean sees ALL task forces
        queryset = TaskForce.objects.all().prefetch_related('departments')
        
        # Filter by Department
        dept_id = self.request.GET.get('department')
        if dept_id:
            queryset = queryset.filter(departments__id=dept_id)
            
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from university.models import Department
        context['departments'] = Department.objects.all()
        return context
