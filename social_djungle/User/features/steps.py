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
#######

@step(r'I try to log in with the user')
def try_to_log_in(step):
    world.browser = Client()
    world.browser.get('/')
    world.response = world.browser.post('/user/login',
                                        {'username' : world.user.username,
                                         'password' : world.user.password })
        
@step(r'The user is authenticated')
def test_if_authenticated(step):
    session = world.browser.session
    session['id'] = 1
    session['user_session'] = 'foo'
    session.set_expiry(0)
    session.save()
    assert Users.is_authenticated(session_key = world.browser.cookies['sessionid'].value, cookie = world.browser.session)
    
@step(r'The cookie should have a "(.*)" field')
def test_cookies_content(step, field):
    sessionInfo = world.browser.session
    assert sessionInfo.get(field, False)
    
@step(r'Finally I log out')
def test_if_logout_works(step):
    world.response = world.browser.get('/user/logout')
    world.browser.session.flush()
    assert not Users.is_authenticated(session_key = world.browser.cookies['sessionid'].value, cookie = world.browser.session)

@step(r'The cookie should not have a "(.*)" field')
def test_cookies_should_not_have(step, field):
    sessionInfo = world.browser.session
    assert not sessionInfo.get(field, False)

#######

@step(r'I create a new user with personal information')
def newUser(step):
    user = Users(email = "foo@bar2.com", username="FooBar2", password = "1234",
                 name = "Someone", surname = "Somebody", birthdate = "1991-12-12",
                 gender = "Hombre", timestamp = datetime.datetime.now())
    world.user2 = user
    world.user2.saveUser()
    
# DateFields:
# If no input_formats argument is provided, the default input formats are:

# '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
# '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
# '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
# '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
# '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'

@step(r'And I retrieve it from the database')
def getUser(step):
    queryset = Users.objects.filter(email = "foo@bar2.com")
    if (queryset):
        world.user2 = queryset.get()

@step(r'Then It should have a name')
def hasName(step):
    assert world.user2.name == 'Someone'
    
@step(r'And It should have a surname')
def hasSurname(step):
    assert world.user2.surname == 'Somebody'
    
@step(r'And It should have a birthdate')
def hasBirthdate(step):
    assert str(world.user2.birthdate) == '1991-12-12'
    
@step(r'And It should have a gender')
def hasGender(step):
    assert world.user2.gender == 'Hombre'
    
###########

@after.all
def cleanDatabase(arg):
    try:
        u1 = Users.objects.get(username = world.user.username)
        u1.delete()
    except:
        pass
    try:
        u2 = Users.objects.get(username = world.user2.username)
        u2.delete()
    except:
        pass