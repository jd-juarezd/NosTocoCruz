from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals
from User.models import Users,ValidationError
import datetime

@step(r'I create a sample user')
def define_user(step):
    u = Users(email = "foo@bar.com", username="FooBar", password = "1234", timestamp=datetime.datetime.now())
    world.user = u
    assert isinstance(u,Users)

@step(r'Then password length is correct')
def pass_long(step):
    assert Users.validatePassword(world.user.password)

@step(r'It should be created correctly')
def create_user(step):
    assert not Users.exists(username=world.user.username)

@step(r'The email cannot be empty')
def empty_field(step):
    world.user.email = ""
    assert not Users.validateEmail(email=world.user.email)
    
@step(r'The email should not be longer than 50 characters')
def right_length(step):
    world.user.email = 'a'*51
    assert not Users.validateEmail(email=world.user.email)
    
@step(r'The email should not accept "(.*)"')
def rigth_format(step, word):
    world.user.email = word
    assert not Users.validateEmail(email=world.user.email)
    
@step(r'And saved')
def save_user(step):
    try:
        world.user.saveUser()
    except ValidationError, e:
        assert not Users.exists(username=world.user.username)
    assert True
    
@step(r'If I try to create it again')
def create_user_again(step):
    u = Users(email = "foo@bar.com", username="FooBar", password = "1234")
    world.user = u
    assert isinstance(u,Users)

@step(r'Then It should not be valid')
def validate_user(step):
    assert Users.exists(username=world.user.username)
    
@after.all
def cleanDatabase(arg):
    q = Users.objects.filter(username=world.user.username)
    if q:
        u = q.get()
        u.delete()
    