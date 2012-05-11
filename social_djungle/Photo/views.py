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

def display (request, photoPath):
    #Añadir aqui comprobaciones respecto a la foto que se pide
    query = Photos.objects.filter(image = photoPath)
    photo = query.get()
    return HttpResponse(photo.image, mimetype="image/png")