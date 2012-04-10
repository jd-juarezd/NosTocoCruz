from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals

#http://tech.yipit.com/2011/12/23/lettuce-best-and-worst-practices-1/
#http://lxml.de/lxmlhtml.html

@before.each_scenario
def prepare_browser(scenario):
    world.browser = Client()

@step(r'I access the url "(.*)"')
def access_url(step, url):
    world.response = world.browser.get(url)
    world.dom = html.fromstring(world.response.content)

@step(r'I see the title "(.*)"')
def see_header(step, text):
    title = world.cssselect('title')[0]
    assert title.text == text

@step(r'There is the form "(.*)"')
def can_log_in(step,formName):
    formulario = world.dom.get_element_by_id(formName)
    world.form = formulario
    assert (formulario != None) and (formulario.tag == 'form')

@step(r'I see a "(.*)" input named "(.*)"')
def see_input(step,inputType,inputId):
    inputs = world.form.inputs
    myInput = inputs[inputId]
    assert myInput.type == inputType
    