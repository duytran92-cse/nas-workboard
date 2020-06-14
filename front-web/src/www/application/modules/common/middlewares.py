import urllib, urllib2, json
from django.contrib.sessions.backends.file import SessionStore
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from django.conf import settings

#class AuthenticationMiddleware(object):
#    def process_request(self, request):
#        if request.get_full_path().startswith('/user'):
#            if request.session.get('user_id', None) is None:
#                return HttpResponseRedirect('/sign-in')
