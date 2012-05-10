# -*- coding: utf-8 -*-
from django.db import models
from User.models import Users
from PIL import Image

class Photos(models.Model):
    name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = 'photos')
    author = models.ForeignKey(Users)

