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
    assert not User.exists(world.user.username)

@step(r'The email cannot be empty')
def empty_field(step):
    world.user.email = ""
    assert not User.validateEmail(world.user.email)
    
@step(r'The email should not be longer than 50 characters')
def right_length(step):
    world.user.email = 'a'*51
    assert not User.validateEmail(world.user.email)
    
@step(r'The email should not accept "(.*)"')
def rigth_format(step, word):
    world.user.email = word
    assert not User.validateEmail(world.user.email)
    
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
    
    