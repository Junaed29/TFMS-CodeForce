from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class RoleRequiredMixin(AccessMixin):
    """Verify that the current user has the required role."""
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if request.user.role != self.required_role:
             # If user is logged in but has wrong role, 403 or redirect to their own dashboard
             # For simplicity here, we raise 403 (Permission Denied) or handle_no_permission
            return self.handle_no_permission()
            
        return super().dispatch(request, *args, **kwargs)
