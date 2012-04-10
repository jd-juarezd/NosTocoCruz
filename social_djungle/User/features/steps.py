from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals

@step(r'I create a sample user')
def define_user(step):
    u = User(email = "foo@bar.com", username="FooBar", password = "1234")
    world.user = u
    assert 1 == 1
    
@step(r'It should be created correctly')
def create_user(step):
    #La clase User ha de tener un metodo que sea is_valid que determine
    #si los campos son correctos
    assert User.exists(world.user.username) and User.validateData(world.user.username, world.user.email, world.user.password)

@step(r'The "(.*)" cannot be empty')
def empty_field(step,field):
    world.user.field = ""
assert User.exists(world.user.username) and User.validateData(world.user.username, world.user.email, world.user.password)
    
@step(r'The "(.*)" should have the right format')
def rigth_format(step,field):
    world.user.field = "foo.@bar"
assert User.exists(world.user.username) and User.validateData(world.user.username, world.user.email, world.user.password)
    


    
    