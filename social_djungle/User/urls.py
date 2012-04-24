from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('User.views',
    url(r'^newuser/?$', 'newUser'),
    url(r'^login/?$', 'login'),
    url(r'^logout/?', 'logout'),
    url(r'^home/?$', 'home'),
    url(r'^config/?$', 'config'),
    url(r'^removeUser/?$', 'removeUser'),
    url(r'^modifypassword/?$', 'modifypassword'),
    url(r'^profile/([0-9]+)/?$', 'profile'),
)