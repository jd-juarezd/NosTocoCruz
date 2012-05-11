from django.conf.urls.defaults import *
from django.conf import settings 
from django.contrib import admin
admin. autodiscover ()

urlpatterns = patterns ('Photo.views',    
      url (r'^(photos/\d+/.+)$', 'display'),
)