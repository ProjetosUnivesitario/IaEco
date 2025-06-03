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

from home.tasks import process_document

from home.filters import *
from home.models import *
from home.serializers import *


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


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    filterset_class = CompanyFilterClass

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class EmissionScopeViewSet(viewsets.ModelViewSet):
    queryset = EmissionScope.objects.all()
    serializer_class = EmissionScopeSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = EmissionScopeFilterClass

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        scope = self.get_object()
        serializer = self.get_serializer(scope)
        return Response(serializer.data)


class EmissionDataViewSet(viewsets.ModelViewSet):
    queryset = EmissionData.objects.all()
    serializer_class = EmissionDataSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = EmissionDataFilterClass

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        emission = self.get_object()
        serializer = self.get_serializer(emission)
        return Response(serializer.data)
    

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        scopes = EmissionScope.objects.filter(company__in=request.user.companies.all()).values(
            'scope_number', 'co2_equivalent', 'progress_percentage'
        )
        total_emissions = EmissionScope.objects.filter(
            company__in=request.user.companies.all()
        ).aggregate(total=Sum('co2_equivalent'))['total'] or 0.0
        return Response({
            'scopes': list(scopes),
            'total_emissions': total_emissions
        })
    

class DocumentUploadViewSet(viewsets.ModelViewSet):
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = DocumentUploadFilterClass

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        document = self.get_object()
        serializer = self.get_serializer(document)
        return Response(serializer.data)
    