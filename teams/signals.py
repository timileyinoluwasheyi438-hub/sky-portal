from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Team, AuditLog

@receiver(post_save, sender=Team)
def log_team_save(sender, instance, created, **kwargs):
    action = f"Team '{instance.name}' was {'created' if created else 'updated'}"
    AuditLog.objects.create(
        action=action,
        details=f"Status: {instance.status} | Department: {instance.department.name}"
    )