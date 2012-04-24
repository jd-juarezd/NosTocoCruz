# -*- coding: utf-8 -*-
from User.models import Users, ValidationError, CookieError
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import hashlib
import datetime
from django.views.decorators.csrf import csrf_protect
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib.sessions.models import Session

@csrf_protect
def newUser(request):
    time = datetime.datetime.now()
    try:
        if (request.POST['password_register'] == request.POST['password_register_checker']):
            encPassword = hashlib.sha1('%s -- %s' % (request.POST['password_register'], str(time))).hexdigest()
            user = Users(username = request.POST['username'],
                         timestamp = time,
                         password = request.POST['password_register'],
                         email = request.POST['email'],
                         name = request.POST['nombre'],
                         surname = request.POST['apellidos'],
                         gender = request.POST['gender'],
                         birthdate = request.POST['birthdate'],
                         inactive = False)
        else:
                raise ValidationError('Las contraseñas no coinciden')
        Users.validateInput(user)
        user.password = encPassword
    except ValidationError as vError:
        request.session['regError'] = 'Los datos de entrada no son válidos'
        return HttpResponseRedirect('/')
    else:
        # User has been created
        try:
            user.saveUser() # and saved to database
        except:
            request.session['regError'] = 'El usuario ya existe en la base de datos.'
        else:
            request.session['newUser'] = True
        return HttpResponseRedirect('/')

"""    
def modifydata(request):
    
    
"""    
def modifypassword(request):
    id = request.session['id']
    user = Users.objects.get(id=id)
    oldpassword = request.POST['old_password']
    newpassword = request.POST['password']
    newpasswordcheck = request.POST['password_checker']
    
    if ((user.matchPassword(oldpassword)) and (newpassword == newpasswordcheck)):
        encPassword = hashlib.sha1('%s -- %s' % (newpassword, str(user.timestamp))).hexdigest()
        user.password = encPassword
        return HttpResponseRedirect('/user/logout')
    else:
        return HttpResponseRedirect('/user/config')

def removeUser(request):
        #User ID
        try:
            id = request.session['id']
        except:
        # User is not logged in
            return HttpResponseRedirect('/')
    
        try:
            user = Users.objects.get(id = id)
        except:
                # User doesn't exist
            return HttpResponseRedirect('/')
        # User has been created
        try:
            user.deleteUser() # and saved to database
            dbCookie = Session.objects.get(session_key = request.session.session_key)
            request.session.flush()
            dbCookie.delete()
        except:
            request.session['regError'] = 'El usuario no existe en la base de datos.'
        return HttpResponseRedirect('/')

@csrf_protect
def login(request):
    if request.session.test_cookie_worked():
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = Users.objects.get(username=username)
        except:
                # User doesn't exist
                return HttpResponseRedirect('/')
                pass
        else:
            if (not user.isInactive()) and (user.matchPassword(password=password)):
                request.session['id'] = str(user.id)
                request.session['user_session'] = user.sessionID()
                request.session.set_expiry(0)
                request.session.delete_test_cookie()   #Clean test cookie
                return HttpResponseRedirect('/user/home')
            else:
                t = get_template('index.html')
                if user.isInactive():
                    c = RequestContext(request, {'errorLogin': 'El usuario está desactivado.'})
                else:
                    c = RequestContext(request, {'errorLogin': 'El usuario y/o la contraseña no son válidos.'})
                return HttpResponse(t.render(c))
    else:
        # Cookies are not enabled!
        t = get_template('index.html')
        c = RequestContext(request, {'errorLogin': 'Debe habilitar las cookies para iniciar sesión.'})
        return HttpResponse(t.render(c))

def logout(request):
    try:
        del request.session['id']
        del request.session['user_session']
    except:
        pass
    else:
        dbSession = Session.objects.get(session_key = request.session.session_key)
        dbSession.delete()
        request.session.flush()
        return HttpResponseRedirect('/')

def home(request):
    try:
        id = request.session['id']
    except:
        # User is not logged in
        return HttpResponseRedirect('/')
    else:
        #User maybe has logged in
        try:
            dbCookie = Session.objects.get(session_key = request.session.session_key).get_decoded()
            if (not Users.is_authenticated(session_key = request.session.session_key, cookie = request.session)):
                raise CookieError
        except:
            # Bad cookie
            request.session.flush()
            return HttpResponseRedirect('/')
        else:
            user = Users.objects.get(id = dbCookie['id'])
            t = get_template('home.html')
            # Here we load all user information with context
            c = RequestContext(request, { 'UserName': user.username,
                                          'UserID': user.id })
            return HttpResponse(t.render(c))

def profile(request, id):
    try:
        user = Users.objects.get(id = id)
        loggedUser = Users.objects.get(id = request.session['id'])
        if (not Users.is_authenticated(session_key = request.session.session_key, cookie = request.session)):
                raise CookieError
    except CookieError:
        # User has not logged in
        request.session.flush()
        return HttpResponseRedirect('/')
    except:
        # Likely, user with id = id has not been found
        return HttpResponseRedirect('/user/home')
    else:
        # Rendering profile page using id
        t = get_template('profile.html')
        c = RequestContext(request, { 'ProfileUserName': user.username,
                                      'ProfileName': user.name,
                                      'ProfileSurname': user.surname,
                                      'ProfileGender': user.gender,
                                      'ProfileBirthdate': user.birthdate,
                                      'UserID': loggedUser.id,
                                      'LoggedUsername': loggedUser.username })
        return HttpResponse(t.render(c))
    
def config(request):
    try:
        id = request.session['id']
    except:
        # User is not logged in
        return HttpResponseRedirect('/')
    else:
        #User maybe has logged in
        try:
            dbCookie = Session.objects.get(session_key = request.session.session_key).get_decoded()
            if (not Users.is_authenticated(session_key = request.session.session_key, cookie = request.session)):
                raise CookieError
        except:
            # Bad cookie
            request.session.flush()
            return HttpResponseRedirect('/')
        else:
            user = Users.objects.get(id = dbCookie['id'])
            t = get_template('config.html')
            # Here we load all user information with context
            c = RequestContext(request, {'UserID': user.id,
                                         'UserName': user.username,
                                         'Name': user.name,
                                         'Surname': user.surname,
                                         'Email': user.email,
                                         'Birthdate': user.birthdate,
                                         'Gender': user.gender })
            return HttpResponse(t.render(c))    
        
        