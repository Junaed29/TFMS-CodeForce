from django.urls import path
from .views import CustomLoginView, ForcePasswordChangeView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('force-password-change/', ForcePasswordChangeView.as_view(), name='force_password_change'),
]
