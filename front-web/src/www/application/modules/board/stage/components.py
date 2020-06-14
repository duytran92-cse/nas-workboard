from django.conf import settings
from application.modules.common import page_contexts

class BoardStageStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        if page_number > 0:
            params['_pager_start'] = (page_number - 1) * 10
            params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/board_stage/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_stage/get', GET={'id': id})
    def get_next_stage(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_stage/get_next_stage', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_stage/create', POST=data)
    def update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_stage/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_stage/delete', POST={'id': id})
    def populate_combobox(self, board_id=0):
        choices = []
        params = {}
        if board_id > 0:
            params['board_id'] = board_id
        records = self.list(sortkey='sort_order', sortdir='asc', params=params, page_number=0)
        for record in records['records']:
            choices.append({
                'id':     record['id'],
                'label':  record['name']
            })
        return choices
