# -*- coding: utf-8 -*-
from django.db import models
from User.models import Users

class Photos(models.Model):
     image = models.ImageField(upload_to = 'photos')
     author = models.ForeignKey(Users)

