# -*- coding: utf-8 -*-
from django.db import models
from User.models import Users
from PIL import Image
import os


def get_upload_path(instance, filename):
    return os.path.join('photos', str(instance.author.id), filename)

class Photos(models.Model):
    name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = get_upload_path)
    author = models.ForeignKey(Users)
    
    def savePhoto(self):
        self.save()

    def __unicode__(self):
        return "%s %s: %s" % (self.name, self.image, self.author)
    
    def deletePhoto(self):
        try:
            self.image.delete()
            self.delete()
        except:
            return "Error borrando la foto, inténtelo de nuevo."
class UserProfilePhoto(models.Model):
    photo = models.ForeignKey(Photos)
    user = models.ForeignKey(Users)
    
    def __unicode__(self):
        return "Foto de perfil de %s" % self.user.username
        