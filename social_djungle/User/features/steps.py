from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals
from User.models import Users,ValidationError

@step(r'I create a sample user')
def define_user(step):
    u = Users(email = "foo@bar.com", username="FooBar", password = "1234")
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

#######

@step(r'I create a new user with personal information')
def newUser(step):
    user = Users(email = "foo@bar.com", username="FooBar", password = "1234",
                 name = "Someone", surname = "Somebody", birthdate = "1991-12-12",
                 gender = "H", country = "Spain")
    world.user = user
    world.user.saveUser()
    
# DateFields:
# If no input_formats argument is provided, the default input formats are:

# '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
# '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
# '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
# '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
# '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'

@step(r'And I retrieve it from the database')
def getUser(step):
    queryset = Users.objects.filter(email = "foo@bar.com")
    if (queryset):
        world.user = queryset.get()

@step(r'Then It should have a name')
def hasName(step):
    assert world.user.name == 'Someone'
    
@step(r'And It should have a surname')
def hasSurname(step):
    assert world.user.surname == 'Somebody'
    
@step(r'And It should have a birthdate')
def hasBirthdate(step):
    assert world.user.birthdate == dateField.new('1991-12-12')
    
@step(r'And It should have a gender')
def hasGender(step):
    assert world.user.gender == 'H'
    
@step(r'And It should have a country')
def hasCountry(step):
    assert world.user.country == 'Spain'
    
###########

@after.all
def cleanDatabase(arg):
    q = Users.objects.filter(username=world.user.username)
    if q:
        u = q.get()
        u.delete()
    