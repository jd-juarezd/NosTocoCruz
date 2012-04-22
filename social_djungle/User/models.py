# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sessions.models import Session
import re
import hashlib
import datetime

class ValidationError(Exception):
    def __init__(self, value):
        self.value = value
class CookieError(Exception):
    def __init__(self, value):
        self.value = value

class Users(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=40) # SHA1 hash is 40 characters long
    timestamp = models.DateTimeField('Account created')
    
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
        valid = (email.__len__() > 0) and (email.__len__() <=50)
        valid = valid and re.match('^(\w|[\._-])+@\w+\.\w+$',email)
        return valid 
    
    @classmethod
    def validatePassword(cls, password):
        if ((password.__len__() < 4) or (password.__len__() > 60)):
            return False
        else:
            # We should check password complexity
            return True
        
    @classmethod
    def validateUsername(cls,username):
        valid = (username.__len__() > 0) and (username.__len__() <= 50)
        valid = valid and re.match('^([a-zA-Z])(\w|[\._-])*', username)
        return valid
        
    @classmethod
    def validateInput(cls, user):
        if (not Users.validateEmail(user.email)):
            raise ValidationError('El email no es válido.')
        if (not Users.validatePassword(user.password)):
            raise ValidationError('La contraseña no es válida. Debe ser de entre 4 y 60 caracteres.')
        if (not Users.validateUsername(user.username)):
            raise ValidationError('El nombre de usuario no es válido.')   
        
    @classmethod
    def is_authenticated(cls, session_key, cookie):
        try:
            dbCookie = Session.objects.get(session_key = session_key).get_decoded()
            if ((dbCookie['id'])
                and (dbCookie['id'] == cookie['id'])):
                return True                
        except:
            return False

    def saveUser(self):
        if (not Users.objects.filter(username=self.username)):
            self.save()
        else:
            raise ValidationError('Ya existe un usuario con ese nombre.')
    
    def matchPassword(self,password):
        encPassw = hashlib.sha1('%s -- %s' % (password, str(self.timestamp))).hexdigest()
        return self.password == encPassw
    
    def sessionID(self):
        id = hashlib.sha1('%s -- %s -- %s' % (self.id,
                                 self.timestamp,
                                 str(datetime.datetime.now()))).hexdigest()
        return id