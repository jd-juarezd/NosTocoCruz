from Micropost.models import Microposts
from User.models import Users
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
import datetime

def newMicropost(request):
    if (request.session.get('id',False) and (Users.objects.filter(id=request.session['id']))): 
        # If user has logged in
        if Microposts.validateLength(request.POST['publication']):
            user = Users.objects.get(id = request.session['id'])
            m = Microposts(author = user,
                           text = request.POST['publication'],
                           date_post = datetime.datetime.now())
            m.save()
        return HttpResponseRedirect("/user/home")
    else:
        HttpResponseRedirect("/")