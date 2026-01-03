from .models import AuditLog

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_action(request, user, action, target_model=None, target_id=None, details=None):
    """
    Helper to log audit events.
    """
    ip = get_client_ip(request) if request else None
    
    AuditLog.objects.create(
        actor=user,
        action=action,
        target_model=target_model,
        target_id=str(target_id) if target_id else None,
        details=details,
        ip_address=ip
    )
