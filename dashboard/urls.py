from django.urls import path
from .views import (
    DashboardDispatcher, AdminDashboardView, HODDashboardView,
    PSMDashboardView, DeanDashboardView, LecturerDashboardView,
    StaffListView, StaffCreateView, TaskForceListView, TaskForceCreateView,
    DepartmentListView, DepartmentCreateView, HODTaskForceListView
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
    path('psm/', PSMDashboardView.as_view(), name='psm'),
    path('dean/', DeanDashboardView.as_view(), name='dean'),
    path('lecturer/', LecturerDashboardView.as_view(), name='lecturer'),
]
