from django.conf.urls.defaults import *
from django.conf import settings 
from django.contrib import admin
admin. autodiscover ()

urlpatterns = patterns ('Photos.views',    
      url (r'^$', 'index'),
      url (r'^display/(?P<id>\d+)/$', 'display'),
)