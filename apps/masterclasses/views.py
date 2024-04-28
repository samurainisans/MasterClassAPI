# views.py
from rest_framework import viewsets
from .models import Category, MasterClass, Participant, Speaker, Organizer
from .serializer import CategorySerializer, ParticipantSerializer, MasterClassSerializer, SpeakerSerializer, \
    OrganizerSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MasterClassViewSet(viewsets.ModelViewSet):
    queryset = MasterClass.objects.all()
    serializer_class = MasterClassSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer


class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer


