from django.contrib import admin

from .models import CustomUser, ModelAuditSettings

admin.site.register(CustomUser)
admin.site.register(ModelAuditSettings)
