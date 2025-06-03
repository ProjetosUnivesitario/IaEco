from auditlog.registry import auditlog
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ModelAuditSettings


@receiver(post_save, sender=ModelAuditSettings)
def manage_auditlog(sender, instance, created, **kwargs):
    if instance.audit_enabled:
        register_auditlog(instance.model_name)
    else:
        unregister_auditlog(instance.model_name)


def register_auditlog(model_name):
    model = apps.get_model('home', model_name)
    auditlog.register(model)
    print(f'Audit log registrado para {model_name}')


def unregister_auditlog(model_name):
    model = apps.get_model('home', model_name)
    auditlog.unregister(model)
    print(f'Audit log desregistrado para {model_name}')
