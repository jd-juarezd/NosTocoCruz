from django.db import models
from User.models import Users
import re
import datetime

# Create your models here.

class Microposts(models.Model):
    id_post = models.IntegerField(primary_key=True)
    author = models.ForeignKey(Users)
    text = models.TextField(max_length=140)
    date_post = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    def __unicode__(self):
        return self.text

    @classmethod
    def validateLength(cls, text):
        if ((text.__len__() < 1) or (text.__len__() > 140)):
            return False
        else:
            return True
        
    @classmethod
    def exists_post(cls, id_post):
        if Microposts.objects.filter(id_post=id_post):
            return True
        else:
            return False
    
#    @classmethod
#    def verify_post(cls, text, id_post):
     
#    @classmethod
#    def verify_owner(cls, id_post):

       