from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals
from Micropost.models import Micropost

@step(r'I create a sample micropost')
def write_micropost(step):
    m = Micropost(author = "1", text = "Hola Mundo", id_post = "12", length = len(text))
    world.micropost = m
    assert isinstance(m,Micropost)
    
@step(r'The text length is correct')
def text_length(step):
    assert Micropost.validateLength(world.micropost.length)
    
@step(r'It should be created correctly')
def create_post(step):
    assert  Micropost.exists_post(id=world.micropost.id_post)
    
@step(r'I published a micropost the written text will be the same as the published text')
def check_post(step):
    assert  Micropost.verify_post(text_post=world.micropost.text,id=world.micropost.id_post)

@step(r'The user that published a micropost will be the owner')
def owner_post(step):
    assert  Micropost.verify_owner(ow=world.micropost.author,id=world.micropost.id_post)