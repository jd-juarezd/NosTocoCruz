from django.conf.urls.defaults import *
from django.conf import settings 
from django.contrib import admin
admin. autodiscover ()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'social_djungle.views.home', name='home'),
    # url(r'^social_djungle/', include('social_djungle.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^user/?', include('User.urls')),
    url(r'^micropost/?', include('Micropost.urls')),
    url(r'^', include('frontend.urls')), 
    url(r'^ $', 'sample.views.index', name = "main-page"),
    url(r'^ display/(? P <id> \ d +)/ $', 'Photo.views.display', name = "display-image")
    
)
