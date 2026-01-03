from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .utils import log_action

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    log_action(request, user, "LOGIN", "User", user.pk, "User logged in successfully")

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    if user:
        log_action(request, user, "LOGOUT", "User", user.pk, "User logged out")

@receiver(user_login_failed)
def log_login_failed(sender, credentials, request, **kwargs):
    # For failed login, we don't have a user object, so we log as System or None
    # We record the attempted username in details
    username = credentials.get('username', 'unknown')
    from .models import AuditLog
    # Create manually since log_action expects a user instance usually
    from .utils import get_client_ip
    ip = get_client_ip(request) if request else None
    AuditLog.objects.create(
        action="LOGIN_FAILED",
        details=f"Failed login attempt for username: {username}",
        ip_address=ip
    )
