import urllib, urllib2, json, jwt
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from django.conf import settings
from application.common import registry

class AuthenticationMiddleware(object):
    def process_request(self, request):
        authorize = False
        global _USER
        if settings.OAUTH_USER_JWT_DEBUG:
            registry.USER = settings.OAUTH_USER_JWT_DEBUG
        else:
            jwt_token = request.COOKIES.get(settings.OAUTH_COOKIE_NAME)
            if jwt_token:
                user = jwt.decode(jwt_token, settings.OAUTH_CLIENT_EK, algorithms=['HS256'])
                if user:
                    authorize = True
                    registry.USER = user
            if not authorize:
                redirect_url = request.GET.get('redirect', settings.APPLICATION_URL)
                sso_server_url = settings.SECURITY_SERVER_URL + '/user/login?redirect=%s' % (redirect_url)
                return HttpResponseRedirect(sso_server_url)
