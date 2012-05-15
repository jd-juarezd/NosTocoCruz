from django.db import models
from User.models import Users

class Messages(models.Model):
    sender = models.ForeignKey(Users, related_name = "messages_sent")
    receiver = models.ForeignKey(Users, related_name = "messages_received")
    text = models.CharField(max_length = 500)
    timestamp = models.DateTimeField()
    
    def __unicode__(self):
        return "Mensaje de %s para %s" % (self.sender.username,self.receiver.username)
    
