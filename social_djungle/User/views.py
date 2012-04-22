# -*- coding: utf-8 -*-
from User.models import Users,ValidationError, CookieError
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
                         password = encPassword,
                         email = request.POST['email'])
        else:
                raise ValidationError('Las contraseñas no coinciden')
        Users.validateInput(user)
    except ValidationError as vError:
        context = {'erroresNuevoUsuario': 'Error de validación'}
        return render(request, 'index.html', context)
    # User has been created
    user.saveUser() # and saved to database
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
            if user.matchPassword(password=password):
                request.session['id'] = str(user.id)
                request.session['user_session'] = user.sessionID()
                request.session.delete_test_cookie()   #Clean test cookie
                request.session.set_expiry(0)
                return HttpResponseRedirect('/home')
            else:
                t = get_template('index.html')
                c = RequestContext(request, {'errorLogin': 'El usuario y/o la contraseña no son válidos'})
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
        return HttpResponseRedirect('/')

def home(request):
    if (not request.session.get('id',False)):
        # User is not logged in
        return HttpResponseRedirect('/')
    else:
        #User maybe has logged in
        try:
            dbCookie = Session.objects.get(session_key = request.session.session_key)
            if not (dbCookie.has_key('user_session') and dbCookie['user_session'] == request.session['user_session']):
                raise CookieError
            if not (dbCookie['id'] == request.session['id']):
                raise CookieError
        except:
            # Bad cookie
            request.session.flush()
            return HttpResponseRedirect('/')
        else:
            user = Users.objects.get(pk = request.session['id'])
            t = get_template('home.html')
            c = RequestContext(request, {'UserName': user.username })
            return HttpResponse(t.render(c))

def profile(request, id):
    pass