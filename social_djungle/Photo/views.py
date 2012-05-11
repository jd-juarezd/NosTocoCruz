# -*- coding: utf-8 -*-
from User.models import Users, ValidationError, CookieError
from Photo.models import Photos
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib.sessions.models import Session
from PIL import Image
import random
INK = "red", "blue", "green", "yellow"

def display (request, photoPath):
    #image = Image.new("RGB", (800, 600), random.choice(INK))
    response = HttpResponse()
    #image.save(response, "PNG")
    query = Photos.objects.filter(image = photoPath)
    photo = query.get()
    image = Image.open(photo.image)
    return HttpResponse(photo.image, mimetype="image/png")