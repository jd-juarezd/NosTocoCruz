# -*- coding: utf-8 -*-
from User.models import Users,ValidationError
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
import hashlib
import datetime

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