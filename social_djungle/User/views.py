# -*- coding: utf-8 -*-
from User.models import Users, Friendships, ValidationError, CookieError
from Micropost.models import Microposts
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import hashlib
import datetime
from django.views.decorators.csrf import csrf_protect
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib.sessions.models import Session

def userIsLogged(request):
    try:
        id = request.session['id']
    except:
        # User is not logged in
        return False
    else:
        return True

def deleteCookie(request):
    dbCookie = Session.objects.get(session_key = request.session.session_key)
    request.session.flush()
    dbCookie.delete()

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

def modifydata(request):
    name = request.POST['name']
    surname = request.POST['surname']
    email = request.POST['email']
    birthdate = request.POST['birthdate']
    gender = request.POST['gender']
    
    user = Users.objects.get(id = request.session['id'])
    if Users.validateEmail(email):
        user.name = name
        user.surname = surname
        user.email = email
        user.birthdate = birthdate
        user.gender = gender
        user.save()
        request.session['configOK'] = 'Los datos se han actualizado satisfactoriamente.'
    else:
        request.session['configError'] = 'El campo email no es válido. Los datos no han sido actualizados.'
    return HttpResponseRedirect('/user/config')
        
def modifypassword(request):
    id = request.session['id']
    user = Users.objects.get(id=id)
    oldpassword = request.POST['old_password']
    newpassword = request.POST['password']
    newpasswordcheck = request.POST['password_checker']
    
    if (Users.validatePassword(newpassword)):
        error = False
        try:
            assert user.matchPassword(oldpassword)
        except:
            error = True
            request.session['passwordError'] = 'La contraseña antigua no coincide.'
            
        try:
            assert newpassword == newpasswordcheck
        except:
            error = True
            request.session['passwordError'] = 'La contraseña nueva no coincide con la confirmación de contraseña.'
            
        if (not error):
            encPassword = hashlib.sha1('%s -- %s' % (newpassword, str(user.timestamp))).hexdigest()
            user.password = encPassword
            user.save()
            request.session['passwordOK'] = 'La contraseña ha sido modificada satisfactoriamente.'
    else:
        request.session['passwordError'] = 'La contraseña no tiene la complejidad requerida.'
    return HttpResponseRedirect('/user/config')

def removeUser(request):
        if (not userIsLogged(request)):
            return HttpResponseRedirect('/')
        
        # If the user is logged, is sure he has a valid id
        user = Users.objects.get(id = request.session['id'])
        
        try:
            user.deleteUser()
            deleteCookie(request)
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
                t = get_template('index.html')
                c = RequestContext(request, {'errorLogin': 'El usuario y/o la contraseña no son válidos.'})
                return HttpResponse(t.render(c))
        else:
            if (not user.isInactive()) and (user.matchPassword(password=password)):
                request.session['id'] = str(user.id)
                request.session['user_session'] = user.sessionID()
                request.session.set_expiry(0)
                request.session.delete_test_cookie()   #Clean test cookie
                return HttpResponseRedirect('/user/home')
            else:
                t = get_template('index.html')
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
        deleteCookie(request)
        return HttpResponseRedirect('/')

def home(request):
    if (not userIsLogged(request)):
        return HttpResponseRedirect("/")
    
    user = Users.objects.get(id = request.session['id'])
    friendsNames = []
    friendships = Friendships.objects.filter(user = user)
    for i in friendships:
        friendsNames += [i.friend.username]
    friendships = Friendships.objects.filter(friend = user)
    for i in friendships:
        friendsNames += [i.user.username]
    friends = Users.objects.filter(username__in = friendsNames)
    # Posts that have to be shown in home page
    userPosts = Microposts.objects.filter(author = user)
    friendPosts = Microposts.objects.filter(author__in=friends)
    posts = userPosts | friendPosts
    posts = posts.order_by('-date_post')
    t = get_template('home.html')
    # Here we load all user information with context
    c = RequestContext(request, { 'UserName': user.username,
                                    'UserID': user.id,
                                    'section': 'Home',
                                    'micropostList': posts })
    return HttpResponse(t.render(c))

def profile(request, id):
    if (not userIsLogged(request)):
        return HttpResponseRedirect("/")
    
    try:
        user = Users.objects.get(id = id)
    except:
        # Likely, user doesn't exist
        return HttpResponseRedirect("/user/home")
    
    loggedUser = Users.objects.get(id = request.session['id'])
    if (not user.inactive):
        # Rendering profile page using id
        t = get_template('profile.html')
        c = RequestContext(request, { 'ProfileUser': user,
                                      'UserID': loggedUser.id,
                                      'UserName': loggedUser.username,
                                      'section': 'Perfil' })
        return HttpResponse(t.render(c))
    else:
        return HttpResponseRedirect('/user/home')
    
def config(request):
    if (not userIsLogged(request)):
        return HttpResponseRedirect("/")
    
    user = Users.objects.get(id = request.session['id'])
    t = get_template('config.html')
    # Here we load all user information with context
    context = {'UserID': user.id,
                'UserName': user.username,
                'Name': user.name,
                'Surname': user.surname,
                'Email': user.email,
                'Birthdate': user.birthdate,
                'Gender': user.gender,
                'section': 'Configuración'}
    
    flags = ['configError', 'configOK', 'passwordError', 'passwordOK']
    for i in flags:
        if (request.session.get(i,False)):
            context.update({ i: request.session[i] })
            del request.session[i]
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))
        