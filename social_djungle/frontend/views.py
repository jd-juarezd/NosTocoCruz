from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.template.loader import get_template

def index(request):
    t = get_template('index.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
    #return render_to_response('index.html')

def profile(request):
    return render_to_response('profile.html')

def home(request):
    return render_to_response('home.html')

def getURL(request, path):
    try:
        t = get_template('%s.html' % str(path))
    except:
        raise Http404
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
    

