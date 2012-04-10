from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals

@step(r'I create a sample user')
def define_user(step):
    u = User(email = "foo@bar.com", username="FooBar", password = "1234")
    world.user = u
    assert isinstance(u,User)
    
@step(r'It should be created correctly')
def create_user(step):
    assert not User.exists(world.user.username) and User.validateData(world.user.username, world.user.email, world.user.password)

@step(r'The "(.*)" cannot be empty')
def empty_field(step,field):
    world.user.field = ""
    assert not User.validateData(world.user.username, world.user.email, world.user.password)
    
@step(r'The "(.*)" should not accept "(.*)"')
def rigth_format(step,field,word):
    world.user.field = word
    assert not User.validateData(world.user.username, world.user.email, world.user.password)
    
@step(r'be saved')
def save_user(step):
    try:
        world.user.save()
    except ValidationError, e:
        assert False
    assert True
    
@step(r'I try to create it again')
def create_user_again(step):
    u = User(email = "foo@bar.com", username="FooBar", password = "1234")
    world.user = u
    assert isinstance(u,User)

@step(r'Then It should not be valid')
def validate_user(step):
    assert User.exists(world.user.name)
    
    