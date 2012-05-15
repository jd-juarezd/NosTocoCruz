# -*- coding: utf-8 -*-
from User.models import Users, Friendships, ValidationError, CookieError
from Micropost.models import Microposts
from Photo.models import Photos
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import hashlib
import datetime
from django.views.decorators.csrf import csrf_protect
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib.sessions.models import Session
from frontend.models import Notifications

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
    
def getFriends(user):
    friendsNames = []
    friendships = Friendships.objects.filter(user = user)
    for i in friendships:
        if i.confirmed:
            friendsNames += [i.friend.username]
    friendships = Friendships.objects.filter(friend = user)
    for i in friendships:
        if i.confirmed:
            friendsNames += [i.user.username]
    friends = Users.objects.filter(username__in = friendsNames)
    return friends

def getNotifications(user):
    # Friendship request notification
    friendshipRequests = Friendships.objects.filter(friend = user, confirmed=False)
    notifications = []
    friendMessage = "Peticion de amistad de"
    m = ""
    addFriendButton = """<a href="/user/acceptFriendship/%s" class="btn btn-success">Aceptar</a>"""
    for i in friendshipRequests:
        m = "%s %s" % (friendMessage, i.user.username)
        notifications += [Notifications(message = m, buttonNeeded = True,  button = addFriendButton % i.pk)]
    return notifications

def renderCookieMessages(request,flags,context):
    for i in flags:
        if (request.session.get(i,False)):
            context.update({ i: request.session[i] })
            del request.session[i]

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
    friends = getFriends(user)
    # Posts that have to be shown in home page
    userPosts = Microposts.objects.filter(author = user)
    friendPosts = Microposts.objects.filter(author__in=friends)
    posts = userPosts | friendPosts
    posts = posts.order_by('-date_post')
    
    # Notifications to the user
    notifications = getNotifications(user)
    
    context = { 'UserName': user.username,
                'UserID': user.id,
                'section': 'Home',
                'micropostList': posts,
                'notifications': notifications }

    # Render possible messages passed by the cookie
    flag = ['friendshipAccepted']
    renderCookieMessages(request,flag,context)
    
    # Here we load all user information with context
    t = get_template('home.html')
    c = RequestContext(request, context)
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
    
    # Profile's Owner microposts
    microposts = Microposts.objects.filter(author=user)
    
    # Check if user is the same or friend of loggedUser
    notFriend = True
    if ((user == loggedUser) or (Friendships.isFriend(user.username, loggedUser.username))):
        notFriend = False
    
    if (not user.inactive):
        # Rendering profile page using id
        t = get_template('profile.html')
        context = { 'ProfileUser': user,
                    'UserID': loggedUser.id,
                    'UserName': loggedUser.username,
                    'section': 'Perfil',
                    'micropostList': microposts,
                    'notFriend': notFriend }
        flags = ['friendshipRequestSent']
        renderCookieMessages(request,flags,context)
        c = RequestContext(request, context)
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
    renderCookieMessages(request,flags, context)
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))

def acceptFriendship(request, friendshipID):
    if (not userIsLogged(request)):
        return HttpResponseRedirect("/")
    
    try:
        friendship = Friendships.objects.get(pk = friendshipID)
    except:
        # Friendship with provided ID doesn't exist
        request.session['friendshipAccepted'] = "Friendship with provided ID doesn't exist"
        pass
    else:
        if (friendship.friend == Users.objects.get(id = request.session['id'])):
            if not friendship.confirmed:
                friendship.confirmed = True
                friendship.save()
                request.session['friendshipAccepted'] = "Se ha aceptado la peticion de amistad de %s" % friendship.user.username
            else:
                request.session['friendshipAccepted'] = 'Error!'
    return HttpResponseRedirect("/user/home")

def sendFriendship(request,profileID):
    if (not userIsLogged(request)):
        return HttpResponseRedirect("/")
    try:
        user = Users.objects.get(id = profileID)
    except:
        # ID doesn't exist
        return HttpResponseRedirect("/user/home")
    
    loggedUser = Users.objects.get(id = request.session['id'])
    
    if not Friendships.isFriend(user.username, loggedUser.username):
        friendship = Friendships(user = loggedUser,
                                friend = user,
                                confirmed = False)
        friendship.save()
        request.session['friendshipRequestSent'] = "La petición se ha enviado correctamente."
    return HttpResponseRedirect("/user/profile/%s/" % profileID)

# DEFINICION INICIAL DE SECCION FOTOS #
def pics(request, id):
    if (not userIsLogged(request)):
        return HttpResponseRedirect("/")
    
    try:
        user = Users.objects.get(id = id)
    except:
        # Likely, user doesn't exist
        return HttpResponseRedirect("/user/home")
    
    loggedUser = Users.objects.get(id = request.session['id'])
    
    # To get to the photo gallery, the user and the owner
    # have to be the same person or friends
    if not ((user == loggedUser) or (Friendships.isFriend(user.username,loggedUser.username))):
        # The gallery can't be accessed by the logged user
        return HttpResponseRedirect("/user/home")
    
    photos = Photos.objects.filter(author=user)
    
    if (not user.inactive):
        # Rendering profile page using id
        t = get_template('pics.html')
        context = { 'ProfileUser': user,
                    'UserID': loggedUser.id,
                    'UserName': loggedUser.username,
                    'photoList': photos,
                    'section': 'Fotos',}
        flags = ['newPhoto','errorPhoto','changeImgOK','changeImgFailed']
        renderCookieMessages(request,flags,context)
        c = RequestContext(request, context)
        return HttpResponse(t.render(c))
    else:
        return HttpResponseRedirect('/user/home')

def uploadPic(request):
    if (not userIsLogged(request)):
        return HttpResponseRedirect("/")

    loggedUser = Users.objects.get(id = request.session['id'])
    photos = Photos.objects.filter(author=loggedUser)
    
    try:
        photo = Photos(name = request.POST['picname'],
                       image = request.FILES['picfile'],
                       author = loggedUser)
        photo.savePhoto()
        request.session['newPhoto'] = "Foto subida con éxito"
    except:
        request.session['errorPhoto'] = "Ha ocurrido un error al subir la foto."
    return HttpResponseRedirect("/user/pics/%i/" % loggedUser.id)

def makeProfileImg(request,imgID):
    if (not userIsLogged(request)):
        return HttpResponseRedirect("/")
    
    loggedUser = Users.objects.get(id = request.session['id'])
    
    try:
        img = Photos.objects.get(id = imgID)
    except:
        # img with id imgID doesn't exist
        pass
    else:
        # Make sure the user is the owner
        if (loggedUser == img.author):
            loggedUser.profilePhoto = img.image.url
            loggedUser.save()
            request.session['changeImgOK'] = "Se ha actualizado su imagen principal."
        else:
            request.session['changeImgFailed'] = "Error al actualizar su imagen principal. Asegúrese de que es el propietario de la imagen."
    return HttpResponseRedirect("/user/pics/%i/" % loggedUser.id)

def people(request, id):
    if (not userIsLogged(request)):
        return HttpResponseRedirect("/")
    
    try:
        user = Users.objects.get(id = id)
    except:
        # Likely, user doesn't exist
        return HttpResponseRedirect("/user/home")
    
    loggedUser = Users.objects.get(id = request.session['id'])
    friendList = getFriends(loggedUser)
    people = Users.objects.all()
    for i in friendList:
        people = people.exclude(username = i.username)
    
    people = people.exclude(username = loggedUser.username)
    
    t = get_template('people.html')
    context = { 'ProfileUser': user,
                'UserID': loggedUser.id,
                'UserName': loggedUser.username,
                'friendList': friendList,
                'section': 'Gente',
                'peopleList': people}
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))

        