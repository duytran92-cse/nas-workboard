from django.conf import settings
from application.modules.common import page_contexts

class UserStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=0):
        if page_number > 0:
            params['_pager_start'] = (page_number - 1) * 10
            params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/user/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/user/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/user/create', POST=data)
    def update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/user/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/user/delete', POST={'user_id': id})
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


class UserFullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(UserFullPageContext, self).__init__()
        self.page_title = 'User'
        self.menu.set_group_selected('user')

        self.breadcrumb.add_entry('user', 'User', '/user/list')
