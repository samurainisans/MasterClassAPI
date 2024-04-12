from rest_framework import generics
from django.db.models import Subquery, OuterRef, Q
from apps.chat.models import ChatMessage
from apps.chat.serializer import MessageSerializer
from apps.users.models import User
from rest_framework import viewsets, mixins, status

class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        messages = ChatMessage.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__reciever=user_id) |
                    Q(reciever__sender=user_id)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), reciever=user_id) |
                            Q(reciever=OuterRef('id'), sender=user_id)
                        ).order_by('-id')[:1].values_list('id', flat=True)
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            )
        ).order_by("-id")

        return messages


class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        reciever_id = self.kwargs['reciever_id']
        messages = ChatMessage.objects.filter(sender__in=[sender_id, reciever_id],
                                              reciever__in=[sender_id, reciever_id])
        return messages


class SendMessagesViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = MessageSerializer

