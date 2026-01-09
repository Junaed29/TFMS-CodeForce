from django.urls import path
from .views import (
    DashboardDispatcher, AdminDashboardView, HODDashboardView,
    PSMDashboardView, DeanDashboardView, LecturerDashboardView,
    StaffListView, StaffCreateView, StaffUpdateView, StaffPasswordResetView, StaffUnlockView, 
    StaffDeactivateView, StaffActivateView, TaskForceListView, TaskForceCreateView,
    TaskForceUpdateView, DepartmentListView, DepartmentCreateView, DepartmentUpdateView, HODTaskForceListView,
    HODTaskForceUpdateView, PSMTaskForceListView, PSMTaskForceDetailView,
    PSMTaskForceModifyView, PSMActionedTaskForceListView, PSMActionedTaskForceUpdateView,
    LecturerTaskForceListView, DeanReportView, AuditLogListView, WorkloadSettingsView
)
from .api import staff_list_api

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardDispatcher.as_view(), name='home'),
    path('audit-logs/', AuditLogListView.as_view(), name='audit_log_list'),
    
    # Admin Views
    path('admin/', AdminDashboardView.as_view(), name='admin'),
    path('admin/staff/', StaffListView.as_view(), name='staff_list'),
    path('admin/staff/add/', StaffCreateView.as_view(), name='staff_add'),
    path("admin/staff/<int:pk>/edit/", StaffUpdateView.as_view(), name="staff_edit"),
    path('admin/staff/<int:pk>/unlock/', StaffUnlockView.as_view(), name='staff_unlock'),
    path('admin/staff/<int:pk>/deactivate/', StaffDeactivateView.as_view(), name='staff_deactivate'),
    path('admin/staff/<int:pk>/activate/', StaffActivateView.as_view(), name='staff_activate'),
    path('admin/staff/<int:pk>/reset-password/', StaffPasswordResetView.as_view(), name='staff_reset_password'),
    path('admin/taskforce/', TaskForceListView.as_view(), name='taskforce_list'),
    path('admin/taskforce/add/', TaskForceCreateView.as_view(), name='taskforce_add'),
    path('admin/taskforce/<int:pk>/edit/', TaskForceUpdateView.as_view(), name='taskforce_edit'),
    path('admin/department/', DepartmentListView.as_view(), name='department_list'),
    path('admin/department/add/', DepartmentCreateView.as_view(), name='department_add'),
    path('admin/department/<int:pk>/edit/', DepartmentUpdateView.as_view(), name='department_edit'),
    path('admin/settings/workload/', WorkloadSettingsView.as_view(), name='workload_settings'),

    # API
    path('api/staff/', staff_list_api, name='staff_list_api'),
    
    # HOD Views
    path('hod/', HODDashboardView.as_view(), name='hod'),
    path('hod/taskforce/', HODTaskForceListView.as_view(), name='hod_taskforce_list'),
    path('hod/taskforce/<int:pk>/manage/', HODTaskForceUpdateView.as_view(), name='hod_taskforce_manage'),
    
    # PSM Views
    path('psm/', PSMDashboardView.as_view(), name='psm'),
    path('psm/approvals/', PSMTaskForceListView.as_view(), name='psm_taskforce_list'),
    path('psm/approvals/<int:pk>/', PSMTaskForceDetailView.as_view(), name='psm_taskforce_review'),
    path('psm/approvals/<int:pk>/modify/', PSMTaskForceModifyView.as_view(), name='psm_taskforce_modify'),
    path('psm/actioned/', PSMActionedTaskForceListView.as_view(), name='psm_taskforce_actioned_list'),
    path('psm/actioned/<int:pk>/', PSMActionedTaskForceUpdateView.as_view(), name='psm_taskforce_actioned_detail'),
    
    
    # Dean Views
    path('dean/', DeanDashboardView.as_view(), name='dean'),
    path('dean/reports/', DeanReportView.as_view(), name='dean_reports'),
    
    # Lecturer Views
    path('lecturer/', LecturerDashboardView.as_view(), name='lecturer'),
    path('lecturer/portfolio/', LecturerTaskForceListView.as_view(), name='lecturer_portfolio'),
]
