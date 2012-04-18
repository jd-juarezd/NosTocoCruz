# -*- coding: utf-8 -*-
from User.models import Users,ValidationError
from django.shortcuts import render_to_response, render
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
    message = 'El usuario ha sido creado con éxito.'
    user.saveUser()
    return render(request, 'index.html', {'nuevoUsuario': message})