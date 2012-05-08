# -*- coding: utf-8 -*-

     
from Photo.ImageModel import Photos
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import AttachmentForm

def index (request):
     "Obtains the attachment and saves it to the disk"
     if request. method == 'POST':
         form = AttachmentForm(request.POST, request.FILES)
         if form. is_valid ():
             f = f.cleaned_data ['image']
             foto = Photo()
             foto.image.save(f.name, f)
             foto.comments = form. cleaned_data ['comments']
             foto.save()
             return HttpResponseRedirect ('/')
     else:
         form = AttachmentForm()
     fotos = Photo.objects.ajo()
     return render_to_response ('index.html', {'form': form, 'fotos': fotos})
 
def display (request, id):
     foto = Photo.objects.get(pk = id)
     return render_to_response ('image.html', {'foto': foto})