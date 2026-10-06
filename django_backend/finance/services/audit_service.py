
from django.utils import timezone

from ..models import AuditLog


def get_client_ip(request):
    return request.META.get("REMOTE_ADDR", "")


def create_audit_log(request, action):
    return AuditLog.objects.create(
        user=request.user,
        action=action,
        ip_address=get_client_ip(request),
        log_time=timezone.now(),
    )
