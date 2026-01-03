from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class RoleRequiredMixin(AccessMixin):
    """
    Mixin to verify that the current user has the required role.
    Also prevents caching to ensure users cannot click 'User' after logout.
    """
    required_role = None

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
            
        if self.required_role and request.user.role != self.required_role:
            # If user has a different role, maybe redirect them to their own dashboard?
            # For now, 403 Forbidden is safer.
            raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)
