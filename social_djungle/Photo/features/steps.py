from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals
from User.models import Users,Friendships,ValidationError
from Photo.models import Photos


# Feature: Testing photo upload and access

@before.all
def setupDB():
    user = Users(email = "correo@correo.com", username="PhotoUser", password = "1234",
                 name = "Someone", surname = "Somebody", birthdate = "1991-12-12",
                 gender = "Hombre", timestamp = datetime.datetime.now())
    user.saveUser()
    world.user = user

# Scenario: Uploading Photo
@step(r'When I upload a photo')
def upload_photo(step):
    photo = Photos(image = 'photos/lion.png' , author = world.user)
    photo.save() 
    
@step(r'Then I can access it')
def get_photo(step):
    query = Photos.objects.filter(author = world.user)
    if (query):
        world.photo = query.get()

# Scenario: Resizing Photo
@step(r'When I try to upload a big photo')
def upload_big_photo(step):
    photo = Photos(image = 'photos/fondo3.png', author = world.user)
    world.photo = photo;
    
@step(r'Then It is resized to a proper size')
def resize_photo(step):
    world.photo.resizePhoto()
    assert ((world.photo.height_field <= 600) & (world.photo.width_field <= 800))

@step(r'And It is correctly saved')
def save(step):
    world.photo.save()
