from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import CustomLoginView
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', RedirectView.as_view(pattern_name='dashboard:home', permanent=False)),  # Redirect root to dashboard (dispatcher)
    
    path('dashboard/', include('dashboard.urls')),
    
    # Password Reset URLs (Django defaults, can keep or move to accounts if needed)
    path('password-reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email.html'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
