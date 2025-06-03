from captcha.helpers import captcha_image_url
from captcha.serializers import CaptchaModelSerializer
from django.contrib.auth.models import User
from rest_framework import serializers

from home.models import *
from .models import Company, EmissionScope, DocumentUpload, EmissionData
import magic



class CaptchaSerializer(serializers.Serializer):
    captcha_key = serializers.CharField()
    captcha_image = serializers.SerializerMethodField()

    def get_captcha_image(self, obj):
        return captcha_image_url(obj['captcha_key'])


class CheckCaptchaModelSerializer(CaptchaModelSerializer):
    sender = serializers.EmailField()

    class Meta:
        model = User
        fields = ('captcha_code', 'captcha_hashkey', 'sender')


class CPFSerializer(serializers.Serializer):
    cpf = serializers.CharField(max_length=14)


class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField(max_length=14)
    password = serializers.CharField(max_length=128)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('As senhas não coincidem.')
        return data

    def validateRepet(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError('Senha não pode ser igual.')
        return data


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUpload
        fields = ['id', 'file_name', 'file_type', 'file_size', 'status', 'created_at', 'error_message']
        read_only_fields = ['id', 'file_type', 'file_size', 'status', 'created_at', 'error_message']

    def validate_file(self, value):
        # Validar tamanho do arquivo (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Arquivo muito grande. Tamanho máximo: 10MB")
        
        # Validar tipo do arquivo
        allowed_types = [
            'application/pdf',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'text/csv',
            'image/jpeg',
            'image/png',
            'image/jpg'
        ]
        
        file_mime = magic.from_buffer(value.read(1024), mime=True)
        value.seek(0)  # Reset file pointer
        
        if file_mime not in allowed_types:
            raise serializers.ValidationError(f"Tipo de arquivo não suportado: {file_mime}")
            
        return value

class EmissionScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionScope
        fields = ['scope_number', 'co2_equivalent', 'progress_percentage', 'year']

class CompanyDashboardSerializer(serializers.ModelSerializer):
    scopes = EmissionScopeSerializer(many=True, read_only=True)
    total_emissions = serializers.SerializerMethodField()
    recent_documents = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'scopes', 'total_emissions', 'recent_documents']
    
    def get_total_emissions(self, obj):
        current_year = 2024
        scopes = obj.scopes.filter(year=current_year)
        return sum(scope.co2_equivalent for scope in scopes)
    
    def get_recent_documents(self, obj):
        recent_docs = obj.documents.order_by('-created_at')[:5]
        return DocumentUploadSerializer(recent_docs, many=True).data