from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=40) # SHA1 hash is 40 characters long
    
    def __unicode__(self):
        return self.username
    
    @classmethod
    def exists(cls, username):
        res = cls.objects.filter(username=username)
        if res:
            return false
        else:
            return true