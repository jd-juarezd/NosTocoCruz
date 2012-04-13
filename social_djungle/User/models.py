from django.db import models
import re

class ValidationError(Exception):
    def __init__(self, value):
        self.value = value
class PasswordError(ValidationError):
    def __init__(self, value):
        self.value = value

class Users(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=40) # SHA1 hash is 40 characters long
    
    def __unicode__(self):
        return self.username
    
    @classmethod
    def exists(cls, username):
        if Users.objects.filter(username=username):
            return True
        else:
            return False
    
    @classmethod
    def validateEmail(cls, email):
        valid = (email.__len__ != 0) & (email.__len__<=50)
        valid = valid and re.match('^(\w|[\._-])+@\w+\.\w+$',email)
        return valid 
    
    @classmethod
    def validatePassword(cls, password):
        if ((password.__len__() < 4) or (password.__len__() > 60)):
            return False
        else:
            return True

    def saveUser(self):
        if (not Users.objects.filter(username=self.username)):
            self.save()
        else:
            raise ValidationError('User already exists in database')