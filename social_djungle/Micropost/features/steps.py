from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals
from Micropost.models import Micropost

@step(r'I create a sample micropost')
def write_micropost(step):
    m = Micropost(author = "1", text = "Hola Mundo")
    world.micropost = m
    assert isinstance(m,Micropost)