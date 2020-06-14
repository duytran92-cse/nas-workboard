from django.conf import settings
from application.modules.common import page_contexts

class BoardTaskStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/board_task/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_task/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_task/create', POST=data)
    def update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_task/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_task/delete', POST={'id': id})
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
