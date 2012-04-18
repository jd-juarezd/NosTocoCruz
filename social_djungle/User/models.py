# -*- coding: utf-8 -*-
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

    def saveUser(self):
        if (not Users.objects.filter(username=self.username)):
            self.save()
        else:
            raise ValidationError('Ya existe un usuario con ese nombre.')