from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('User.views',
    url(r'^newuser/?$', 'newUser'),
    url(r'^login/?$', 'login'),
    url(r'^logout/?', 'logout'),
    url(r'^home/?$', 'home'),
    url(r'^config/?$', 'config'),
    url(r'^removeUser/?$', 'removeUser'),
    url(r'^modifypassword/?$', 'modifypassword'),
    url(r'^modifydata/?$', 'modifydata'),
    url(r'^profile/([0-9]+)/?$', 'profile'),
    url(r'^acceptFriendship/([0-9]+)/?', 'acceptFriendship'),
    url(r'^sendFriendship/([0-9]+)/?', 'sendFriendship'),
    #DEFINICION INICIAL DE SECCION FOTOS
    url(r'^pics/([0-9]+)/?$', 'pics'),
    url(r'^makeProfileImg/([0-9]+)/?', 'makeProfileImg'),
    url(r'^makeBackgroundImg/([0-9]+)/?', 'makeBackgroundImg'),
    url(r'^uploadpic/?$', 'uploadPic'),
    url(r'^people/([0-9]+)/?$', 'people'),
    url(r'^messages/?$', 'messages'),
)