from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('Micropost.views',
    url(r'^new/?$', 'newMicropost'),
)