from django.urls import path
from .views import (
    DashboardDispatcher, AdminDashboardView, HODDashboardView,
    PSMDashboardView, DeanDashboardView, LecturerDashboardView
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardDispatcher.as_view(), name='home'),
    path('admin/', AdminDashboardView.as_view(), name='admin'),
    path('hod/', HODDashboardView.as_view(), name='hod'),
    path('psm/', PSMDashboardView.as_view(), name='psm'),
    path('dean/', DeanDashboardView.as_view(), name='dean'),
    path('lecturer/', LecturerDashboardView.as_view(), name='lecturer'),
]
