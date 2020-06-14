from django.conf import settings
from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer

from application.modules.common import page_contexts
from django.conf import settings
from application.common import registry

class QueueStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/queue/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue/create', POST=data)
    def update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue/delete', POST={'id': id})
    def populate_combobox(self):
        choices = []
        params = {}
        records = self.list(sortkey='name', sortdir='asc', params=params)
        for record in records['records']:
            choices.append({
                'id':     record['id'],
                'label':  record['name']
            })
        return choices


class QueueFullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(QueueFullPageContext, self).__init__()
        self.renderer.template = 'workboard/queue/page_contexts.html'

        self.queue_id = params['queue_id']
        self.queue = QueueStore(container).get(params['queue_id'])['data']['record']
        self.menu = params['submenu']

        # User
        self.user = registry.USER
        self.user['logout_link'] = settings.SECURITY_SERVER_URL + '/user/logout?redirect=%s' % (settings.APPLICATION_URL)
