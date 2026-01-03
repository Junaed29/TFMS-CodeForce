from django.urls import path
from .views import (
    DashboardDispatcher, AdminDashboardView, HODDashboardView,
    PSMDashboardView, DeanDashboardView, LecturerDashboardView,
    StaffListView, StaffCreateView, TaskForceListView, TaskForceCreateView,
    DepartmentListView, DepartmentCreateView, HODTaskForceListView,
    HODTaskForceUpdateView, PSMTaskForceListView, PSMTaskForceDetailView,
    LecturerTaskForceListView, DeanReportView
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardDispatcher.as_view(), name='home'),
    
    # Admin Views
    path('admin/', AdminDashboardView.as_view(), name='admin'),
    path('admin/staff/', StaffListView.as_view(), name='staff_list'),
    path('admin/staff/add/', StaffCreateView.as_view(), name='staff_add'),
    path('admin/taskforce/', TaskForceListView.as_view(), name='taskforce_list'),
    path('admin/taskforce/add/', TaskForceCreateView.as_view(), name='taskforce_add'),
    path('admin/department/', DepartmentListView.as_view(), name='department_list'),
    path('admin/department/add/', DepartmentCreateView.as_view(), name='department_add'),

    # HOD Views
    path('hod/', HODDashboardView.as_view(), name='hod'),
    path('hod/taskforce/', HODTaskForceListView.as_view(), name='hod_taskforce_list'),
    path('hod/taskforce/<int:pk>/manage/', HODTaskForceUpdateView.as_view(), name='hod_taskforce_manage'),
    
    # PSM Views
    path('psm/', PSMDashboardView.as_view(), name='psm'),
    path('psm/approvals/', PSMTaskForceListView.as_view(), name='psm_taskforce_list'),
    path('psm/approvals/<int:pk>/', PSMTaskForceDetailView.as_view(), name='psm_taskforce_review'),
    
    
    # Dean Views
    path('dean/', DeanDashboardView.as_view(), name='dean'),
    path('dean/reports/', DeanReportView.as_view(), name='dean_reports'),
    
    # Lecturer Views
    path('lecturer/', LecturerDashboardView.as_view(), name='lecturer'),
    path('lecturer/portfolio/', LecturerTaskForceListView.as_view(), name='lecturer_portfolio'),
]
