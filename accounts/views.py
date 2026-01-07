from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """
        Security: Reset failed attempts on successful login.
        Check if user is locked effectively (double check).
        """
        user = form.get_user()
        if user.is_locked and not (user.is_superuser or user.role == User.Role.ADMIN):
            messages.error(self.request, "Your account has been locked due to multiple failed login attempts. Please contact the Administrator.")
            return self.form_invalid(form)
            
        # Reset attempts on success
        if user.failed_attempts > 0:
            user.failed_attempts = 0
            user.save()
            
        if user.must_change_password:
            from django.contrib.auth import login
            login(self.request, user)
            return redirect('force_password_change')
            
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Security: Increment failed attempts on failed login.
        Lock account if attempts >= 3.
        """
        username = form.data.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                
                # Admin Exception: Admins never get locked
                if user.is_superuser or user.role == User.Role.ADMIN:
                    return super().form_invalid(form)
                
                if user.is_locked:
                    messages.error(self.request, "Your account has been locked due to multiple failed login attempts. Please contact the Administrator.")
                else:
                    user.failed_attempts += 1
                    if user.failed_attempts >= 3:
                        user.is_locked = True
                        user.save()
                        messages.error(self.request, "Your account has been locked due to multiple failed login attempts. Please contact the Administrator.")
                    else:
                        user.save()
                        # Optional: Tell them how many attempts left? maybe not for security obscuration.
                        
            except User.DoesNotExist:
                # Do nothing if user doesn't exist (prevent enumeration timing attacks ideally, but simple here)
                pass
                
        return super().form_invalid(form)

from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ForcePasswordChangeView(LoginRequiredMixin, FormView):
    template_name = 'registration/force_password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('dashboard:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        # Update session to prevent logging out
        update_session_auth_hash(self.request, user)
        
        # Unset the flag
        user.must_change_password = False
        user.save()
        
        messages.success(self.request, "Password changed successfully. You can now access the dashboard.")
        log_action(self.request, user, "CHANGE_PASSWORD", "User", user.pk, "User changed password via forced flow")
        
        return super().form_valid(form)

from accounts.utils import log_action
