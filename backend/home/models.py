from django.contrib.auth.models import AbstractUser, User
from django.db import models
import uuid


class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)
    is_temporary_password = models.BooleanField(default=False)

    class Meta:
        db_table = 'customuser'

    def __str__(self):
        return self.username


class ModelAuditSettings(models.Model):
    model_name = models.CharField(max_length=100)
    audit_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'model_audit_settings'

    def __str__(self):
        return f'{self.model_name} - {"Ativado" if self.audit_enabled else "Desativado"}'


class Company(models.Model):
    name = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

class EmissionScope(models.Model):
    SCOPE_CHOICES = [
        (1, 'Escopo 1 - Emissões Diretas'),
        (2, 'Escopo 2 - Emissões Indiretas (Energia)'),
        (3, 'Escopo 3 - Outras Emissões Indiretas'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='scopes')
    scope_number = models.IntegerField(choices=SCOPE_CHOICES)
    co2_equivalent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    progress_percentage = models.IntegerField(default=0)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - Escopo {self.scope_number} - {self.year}"

    class Meta:
        unique_together = ['company', 'scope_number', 'year']

class DocumentUpload(models.Model):
    FILE_TYPE_CHOICES = [
        ('PDF', 'PDF Document'),
        ('EXCEL', 'Excel Spreadsheet'), 
        ('CSV', 'CSV File'),
        ('IMAGE', 'Image File'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PROCESSING', 'Processando'),
        ('COMPLETED', 'Concluído'),
        ('FAILED', 'Falhou'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    file_size = models.BigIntegerField()  # em bytes
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    task_id = models.CharField(max_length=255, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    processed_data = models.JSONField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.file_name} - {self.status}"

class EmissionData(models.Model):
    document = models.ForeignKey(DocumentUpload, on_delete=models.CASCADE, related_name='emissions')
    scope = models.ForeignKey(EmissionScope, on_delete=models.CASCADE, related_name='data_entries')
    source_category = models.CharField(max_length=100)  # ex: "Combustão Estacionária"
    co2_value = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=20, default='tCO₂e')
    calculation_method = models.CharField(max_length=100, null=True, blank=True)
    raw_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.scope} - {self.source_category}: {self.co2_value} {self.unit}"
