from captcha.helpers import captcha_image_url
from captcha.serializers import CaptchaModelSerializer
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from home.tasks import process_document
from home.models import *

import pika
import json
import uuid
import os
from django.conf import settings


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


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'cnpj', 'created_at', 'updated_at']

class EmissionScopeSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = EmissionScope
        fields = ['id', 'company', 'scope_number', 'co2_equivalent', 'progress_percentage', 'year', 'created_at', 'updated_at']

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUpload
        fields = ['id', 'company', 'file', 'file_name', 'file_type', 'file_size', 'status', 'error_message', 'processed_data', 'uploaded_by', 'created_at', 'updated_at']
        read_only_fields = ['status', 'error_message', 'processed_data', 'created_at', 'updated_at']

    def create(self, validated_data):
        document = DocumentUpload.objects.create(**validated_data)
        # Publish to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue='document_processing', durable=True)
        message = {
            'document_id': str(document.id),
            'file_path': document.file.path,
            'file_type': document.file_type,
        }
        channel.basic_publish(
            exchange='',
            routing_key='document_processing',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
        )
        connection.close()
        return document

class EmissionDataSerializer(serializers.ModelSerializer):
    scope = EmissionScopeSerializer(read_only=True)
    
    class Meta:
        model = EmissionData
        fields = ['id', 'document', 'scope', 'source_category', 'co2_value', 'unit', 'calculation_method', 'raw_data', 'created_at']


class DocumentUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(source='file', write_only=True)

    class Meta:
        model = DocumentUpload
        fields = ['id', 'company', 'file', 'file_name', 'file_type', 'file_size', 'status', 'error_message', 'processed_data', 'uploaded_by', 'created_at', 'updated_at']
        read_only_fields = ['status', 'error_message', 'processed_data', 'file_name', 'file_type', 'file_size', 'uploaded_by', 'created_at', 'updated_at']

    def validate_file(self, value):
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Arquivo muito grande. Tamanho máximo: 10MB.")
        return value

    def create(self, validated_data):
        file = validated_data.pop('file')
        file_name = file.name
        file_type = os.path.splitext(file_name)[1].lstrip('.').upper() or 'UNKNOWN'
        file_size = file.size

        document = DocumentUpload.objects.create(
            company=validated_data['company'],
            file=file,
            file_name=file_name,
            file_type=file_type,
            file_size=file_size,
            uploaded_by=self.context['request'].user
        )
        process_document.delay(str(document.id), document.file.path, document.file_type)
        return document
