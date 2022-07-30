from django.db import models


class Message(models.Model):
    sender = models.CharField(max_length=60)
    receiver = models.CharField(max_length=60)
    # requirements assumption:
    # max length of the body is 160 because that's the standard for text messages
    # TODO-PRODUCTIONIZATION - move from hardcoded to config max_length values
    body = models.CharField(max_length=160)
    # could make received a DateTime as well, but boolean now for simplicity
    received = models.BooleanField(default=False, editable=False)
    # track system created/modified times - based on processing time 
    # https://www.django-rest-framework.org/api-guide/fields/#datetimefield
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return "S: "+self.sender+" R: "+self.receiver+" Created: "+str(self.created);
