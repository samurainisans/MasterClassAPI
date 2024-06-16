# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/users/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from .serializer import PasswordResetSerializer, PasswordResetConfirmSerializer, UserRegistrationSerializer, \
    LoginSerializer, UserDetailSerializer
from ..masterclasses.models import FavoriteMasterClass
from ..masterclasses.serializer import FavoriteMasterClassSerializer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .models import User, Role, Contact
from .serializer import UserSerializer, RoleSerializer, ContactSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from rest_framework.generics import GenericAPIView


# Восстановление пароля
class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь с таким email не найден'}, status=status.HTTP_400_BAD_REQUEST)

            current_site = get_current_site(request)
            mail_subject = 'Сброс пароля'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            return Response({'message': 'Письмо с инструкциями по сбросу пароля отправлено'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# подтверждение смены пароля
class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                password = serializer.validated_data['password']
                user.set_password(password)
                user.save()
                return Response({'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Некорректная ссылка или токен'}, status=status.HTTP_400_BAD_REQUEST)


# Регистрация пользователя
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Подтвердите учётную запись'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"  # this is the crucial part
        email.send()
        return Response({'message': 'Пользователь успешно зарегистрирован. Проверьте почту для подтверждения аккаунта'},
                        status=status.HTTP_201_CREATED)


# Верификация аккаунта
class ActivateView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.verified = True
            user.save()
            return Response({'message': 'Учётная запись успешно подтверждена'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Неккоректная ссылка'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMasterClass.objects.all()
    serializer_class = FavoriteMasterClassSerializer


class SpeakerViewSet(viewsets.ViewSet):
    def list(self, request):
        speakers = User.objects.filter(role__name='Speaker')
        serializer = UserSerializer(speakers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganizerViewSet(viewsets.ViewSet):
    def list(self, request):
        organizers = User.objects.filter(role__name='Organizer')
        serializer = UserSerializer(organizers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': _('Неверные учетные данные')}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': _('Аккаунт не активирован. Проверьте почту для подтверждения.')},
                            status=status.HTTP_403_FORBIDDEN)

        if not user.verified:
            return Response({'error': _('Аккаунт не подтвержден. Проверьте почту для подтверждения.')},
                            status=status.HTTP_403_FORBIDDEN)

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': _('Неверные учетные данные')}, status=status.HTTP_401_UNAUTHORIZED)
