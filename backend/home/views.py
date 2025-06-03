from functools import reduce
from smtplib import SMTPException

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from dj_rql.drf import RQLFilterBackend
from dj_rql.filter_cls import RQLFilterClass
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Count, DecimalField, F, OuterRef, Subquery, Sum
from django.db.models.expressions import ExpressionWrapper
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from home.models import CustomUser
from home.serializers import (CaptchaSerializer,
                              ChangePasswordSerializer,
                              CPFSerializer, LoginSerializer)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                'first_name': user.first_name.capitalize(),
                'last_name': user.last_name.capitalize(),
            }
        )


class CaptchaView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        captcha_key = CaptchaStore.generate_key()
        captcha_image_url1 = captcha_image_url(captcha_key)

        data = {
            'captcha_key': captcha_key,
            'captcha_image': captcha_image_url1,
        }

        serializer = CaptchaSerializer(data)
        return Response(serializer.data)


class ValidateCaptchaView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        captcha_key = request.data.get('captcha_key')
        captcha_value = request.data.get('captcha_value')

        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
            if captcha.response == captcha_value.lower():
                captcha.delete()
                return Response(
                    {'message': 'Captcha válido'}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Captcha inválido'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except CaptchaStore.DoesNotExist:
            return Response(
                {'message': 'Captcha inválido'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AuthResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CPFSerializer(data=request.data)
        if serializer.is_valid():
            cpf = serializer.validated_data['cpf']
            try:
                with transaction.atomic(using='default'):
                    usuario = CustomUser.objects.using('default').get(cpf=cpf)
                    senha_temporaria = get_random_string(8)
                    usuario.set_password(senha_temporaria)
                    usuario.is_temporary_password = True
                    usuario.save(using='default')
                try:
                    send_mail(
                        'Redefinição de Senha',
                        f'Use a seguinte senha temporária para acessar: {senha_temporaria}.',
                        'jefferson.guedes@sepog.fortaleza.ce.gov.br',
                        [usuario.email],
                        fail_silently=False,
                    )
                    return Response(
                        {
                            'message': 'Um e-mail com a senha temporária foi enviado.'
                        },
                        status=status.HTTP_200_OK,
                    )
                except SMTPException as e:
                    return Response(
                        {
                            'message': 'Senha temporária gerada, mas o e-mail não pôde ser enviado.',
                            'error': str(e),
                        },
                        status=status.HTTP_200_OK,
                    )
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'CPF não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class AuthLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            cpf = serializer.validated_data['cpf']
            password = serializer.validated_data['password']
            user = CustomUser.objects.get(cpf=cpf)

            if check_password(password, user.password):
                if user.is_temporary_password:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            'message': 'Login bem-sucedido. Redirecionando para alteração de senha.',
                            'auth_login': 'auth_register',
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            'message': 'Login bem-sucedido. Redirecionando para a página inicial.',
                            'auth_login': 'access',
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                        },
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                    {'error': 'CPF ou senha incorretos.'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            if not user.check_password(
                serializer.validated_data['old_password']
            ):
                return Response(
                    {'error': 'A senha atual está incorreta.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(serializer.validated_data['new_password'])
            user.is_temporary_password = False
            user.save()

            update_session_auth_hash(request, user)

            return Response(
                {'message': 'Senha alterada com sucesso.'},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class DocumentUploadView(generics.CreateAPIView):
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        try:
            files = request.FILES.getlist('files')
            if not files:
                return Response(
                    {'error': 'Nenhum arquivo foi enviado'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            uploaded_docs = []
            
            # Obter ou criar empresa padrão
            company, created = Company.objects.get_or_create(
                name="Empresa Padrão",
                defaults={'cnpj': None}
            )

            for file in files:
                # Determinar tipo do arquivo
                file_type = self.determine_file_type(file)
                
                # Criar documento
                document = DocumentUpload.objects.create(
                    company=company,
                    file=file,
                    file_name=file.name,
                    file_type=file_type,
                    file_size=file.size,
                    uploaded_by=request.user if request.user.is_authenticated else None
                )
                
                # Enviar para processamento em background
                task = process_carbon_document.delay(str(document.id))
                document.task_id = task.id
                document.save()
                
                uploaded_docs.append({
                    'id': str(document.id),
                    'file_name': document.file_name,
                    'file_type': document.file_type,
                    'status': document.status,
                    'task_id': task.id
                })

            return Response({
                'message': f'{len(uploaded_docs)} arquivo(s) enviado(s) com sucesso!',
                'documents': uploaded_docs
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': f'Erro ao fazer upload: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def determine_file_type(self, file):
        """Determinar o tipo do arquivo baseado no MIME type"""
        file_mime = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)  # Reset file pointer
        
        mime_to_type = {
            'application/pdf': 'PDF',
            'application/vnd.ms-excel': 'EXCEL',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'EXCEL',
            'text/csv': 'CSV',
            'image/jpeg': 'IMAGE',
            'image/png': 'IMAGE',
            'image/jpg': 'IMAGE',
        }
        
        return mime_to_type.get(file_mime, 'OTHER')

@api_view(['GET'])
def dashboard_data(request):
    """Endpoint para dados do dashboard"""
    try:
        # Obter empresa padrão
        company = Company.objects.filter(name="Empresa Padrão").first()
        
        if not company:
            # Criar dados demo se não existir
            company = Company.objects.create(name="Empresa Padrão")
            
            # Criar escopos demo
            current_year = 2024
            EmissionScope.objects.create(
                company=company, scope_number=1, co2_equivalent=735.0, 
                progress_percentage=100, year=current_year
            )
            EmissionScope.objects.create(
                company=company, scope_number=2, co2_equivalent=625.0, 
                progress_percentage=100, year=current_year
            )
            EmissionScope.objects.create(
                company=company, scope_number=3, co2_equivalent=1285.0, 
                progress_percentage=92, year=current_year
            )
        
        serializer = CompanyDashboardSerializer(company)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': f'Erro ao obter dados do dashboard: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def document_status(request, document_id):
    """Verificar status de processamento de um documento"""
    try:
        document = DocumentUpload.objects.get(id=document_id)
        serializer = DocumentUploadSerializer(document)
        return Response(serializer.data)
    except DocumentUpload.DoesNotExist:
        return Response(
            {'error': 'Documento não encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )