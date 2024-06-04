# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/users/views.py
from rest_framework import viewsets
from .models import User, Role, Contact
from .serializer import UserSerializer, RoleSerializer, ContactSerializer
from ..masterclasses.models import Category, FavoriteMasterClass
from ..masterclasses.serializer import CategorySerializer, FavoriteMasterClassSerializer
from rest_framework import viewsets
from .models import User, Role, Contact
from .serializer import UserSerializer, RoleSerializer, ContactSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics, status
from rest_framework.response import Response
from .serializer import UserRegistrationSerializer
from django.core.mail import EmailMessage

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


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMasterClass.objects.all()
    serializer_class = FavoriteMasterClassSerializer
