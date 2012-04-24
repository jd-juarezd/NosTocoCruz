from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals
from Micropost.models import Microposts, MicropostError
from User.models import Users
import datetime

@before.all
def setUp():
    user = Users(username = 'TestUser',
                 password = '1234',
                 email = 'testuser@testuser.com',
                 name = 'testuser',
                 surname = 'testUser',
                 gender = 'Hombre',
                 timestamp = datetime.datetime.now())
    world.user = user
    user.save()

@step(r'I create a sample micropost')
def write_micropost(step):
    m = Microposts(author = world.user, text = "Hola Mundo", id_post = "12", date_post = datetime.datetime.now())
    world.micropost = m
    assert isinstance(m,Microposts)
    world.micropost.save()
    
@step(r'Then The text length is correct')
def text_length(step):
    assert Microposts.validateLength(world.micropost.text)
    
@step(r'Then micropost should be created correctly')
def create_post(step):
    assert  Microposts.exists(id_post=world.micropost.id_post)
    
@step(r'When I publish a micropost the written text will be the same as the published text')
def check_post(step):
    try:
        dbMicropost = Microposts.objects.get(id_post = world.micropost.id_post)
    except:
        raise MicropostError('El micropost no existe en la base de datos')
    else:
        assert dbMicropost.text == world.micropost.text

@step(r'The user that published a micropost will be the owner')
def owner_post(step):
    try:
        dbMicropost = Microposts.objects.get(id_post = world.micropost.id_post)
    except:
        raise MicropostError('El micropost no existe en la base de datos')
    else:
        assert dbMicropost.author == world.micropost.author
        
@after.all
def cleaning(arg):
    try:
        user = Users.objects.get(username = world.user.username)
    except:
        pass
    else:
        user.delete()
    try:
        micropost = Microposts.objects.get(id_post = world.micropost.id_post)
    except:
        pass
    else:
        micropost.delete()