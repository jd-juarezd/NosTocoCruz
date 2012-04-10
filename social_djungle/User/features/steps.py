from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals

@step(r'I create a sample user')
def create_user(step):
    u = User(email = "foo@bar.com", username="FooBar")
    world.user = u
    