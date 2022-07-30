from datetime import datetime, timedelta

from .models import Message


DEFAULT_MAX_DAYS_OLD = 30
DEFAULT_RESULT_LIMIT = 100


class QuerySetFilters():
 
    def filter_by_receiver(path_params, query_params, queryset):
        '''
        If a receiver is specified in the path or query params,
        reduces the queryset to only the messages where the receiver
        matches the value specified.
        Otherwise returns the current queryset unaltered. 
        '''
        receiver = path_params.get("receiver", None)
        # if receiver not in URL, check query param
        if receiver is None:
            receiver = query_params.get('receiver', None)

        if receiver is not None:
            return queryset.filter(receiver=receiver)
        return queryset


    def filter_by_sender(query_params, queryset):
        '''
        If a sender is specified in query parameters, reduce
        the queryset to only the messages with that sender,
        otherwise returns the current queryset unaltered.
        '''
        sender = query_params.get('sender', None)
        if sender is not None:
            return queryset.filter(sender=sender)
        return queryset


    def filter_by_message_age(query_params, queryset):
        '''
        Reduce the queryset to messages that are up to
        the default days old unless the max days old
        is specified in the query params.
        '''
        max_days = DEFAULT_MAX_DAYS_OLD
        max_days_old = query_params.get('max_days_old', None)
        if max_days_old is not None:
            try:
                max_days = int(max_days_old)
            except:
                print("Invalid value for max_days_old: "+str(max_days_old))
                max_days = DEFAULT_MAX_DAYS_OLD

        oldest_datetime = datetime.today() - timedelta(days=max_days)
        return queryset.filter(created__gte=oldest_datetime)


    def filter_by_unreceived(query_params, queryset):
        '''
        If request query params specify only_unreceived, 
        then reduce the queryset to only the messages that
        are not flagged as received already.
        '''
        only_unreceived = query_params.get('only_unreceived', None)
        if only_unreceived is not None:
            return queryset.filter(received=False)
        return queryset

