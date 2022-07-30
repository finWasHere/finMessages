from datetime import datetime, timedelta
from rest_framework import viewsets

from .filters import QuerySetFilters
from .models import Message
from .serializers import MessageSerializer


class ReceiveViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('created')
    serializer_class = MessageSerializer
    http_method_names = ['get']

    def get_queryset(self):
        r_queryset = super().get_queryset()

        # TODO - encapsulate the path & query params in a request parser object, just pass that to the filters
        r_queryset = QuerySetFilters.filter_by_receiver(self.kwargs, self.request.query_params, r_queryset)
        r_queryset = QuerySetFilters.filter_by_sender(self.request.query_params, r_queryset)
        r_queryset = QuerySetFilters.filter_by_message_age(self.request.query_params, r_queryset)
        r_queryset = QuerySetFilters.filter_by_unreceived(self.request.query_params, r_queryset)

        r_receiver = self.kwargs.get("receiver", None)
        if r_receiver is not None:
        	# we will only mark messages as received if they were 
        	# accessed via the query path
            # update the received flag
            # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#django.db.models.query.QuerySet.update
            update_count = r_queryset.update(received=True)
            print("Unread Messages Received: "+str(update_count))

        return r_queryset


class CreateViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    http_method_names = ['post']

