from django.conf import settings
from application.modules.common import page_contexts

class QueueStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        if page_number > 0:
            params['_pager_start'] = (page_number - 1) * 10
            params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/queue/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue/get', GET={'id': id})
    def get_summary(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue/get_summary', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue/create', POST=data)
    def update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue/delete', POST={'id': id})
    def populate_combobox(self):
        choices = []
        params = {}
        records = self.list(sortkey='name', sortdir='asc', params=params, page_number=0)
        for record in records['records']:
            choices.append({
                'id':     record['id'],
                'label':  record['name']
            })
        return choices


class QueueFullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(QueueFullPageContext, self).__init__()
        self.page_title = 'Queue'
        self.menu.set_group_selected('queue')

        self.breadcrumb.add_entry('queue', 'Queue', '/queue/list')
        if 'queue_id' in params and params['queue_id']:
            self.submenu.create_menu_group('update', 'Queue', '/queue/update/%s' % (str(params['queue_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('request', 'Request', '/queue/detail/%s/request/list' % (str(params['queue_id'])), 'zmdi-border-all')
            self.submenu.set_group_selected(params['submenu'])
