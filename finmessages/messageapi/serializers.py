from rest_framework import serializers

from .models import Message

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'body', 'received', 'created', 'modified')
