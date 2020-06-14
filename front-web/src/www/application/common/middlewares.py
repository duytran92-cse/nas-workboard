import urllib, urllib2, json, jwt
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from django.conf import settings
from application.common import registry

class AuthenticationMiddleware(object):
    def call_api(self, url, POST=None, GET={}):
        if POST is not None:
            req = urllib2.Request(url, json.dumps(POST))
            res = urllib2.urlopen(req)
            data = json.loads(res.read())
            return data
        else:
            res = urllib.urlopen(url + '?' + urllib.urlencode(GET))
            data = res.read()
            data = json.loads(data)
            return data

    def process_request(self, request):
        authorize = False
        global _USER
        if settings.OAUTH_USER_JWT_DEBUG:
            registry.USER = settings.OAUTH_USER_JWT_DEBUG
            data = self.call_api(settings.WORKBOARD_API_URL + '/user/get_by_username', GET={'username': registry.USER['username']})
            if not data['data']['record']['id']:
                return HttpResponse('Access denied!')
            registry.USER['user_id'] = data['data']['record']['id']
        else:
            jwt_token = request.COOKIES.get(settings.OAUTH_COOKIE_NAME)
            if jwt_token:
                user = jwt.decode(jwt_token, settings.OAUTH_CLIENT_EK, algorithms=['HS256'])
                if user:
                    authorize = True
                    registry.USER = user
                    data = self.call_api(settings.WORKBOARD_API_URL + '/user/get_by_username', GET={'username': registry.USER['username']})
                    if not data['data']['record']['id']:
                        return HttpResponse('Access denied!')
                    registry.USER['user_id'] = data['data']['record']['id']
            if not authorize:
                redirect_url = request.GET.get('redirect', settings.APPLICATION_URL)
                sso_server_url = settings.SECURITY_SERVER_URL + '/user/login?redirect=%s' % (redirect_url)
                return HttpResponseRedirect(sso_server_url)
