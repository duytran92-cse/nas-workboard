from django.conf import settings

class BoardEventStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        if page_number > 0:
            params['_pager_start'] = (page_number - 1) * 10
            params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/board_event/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_event/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_event/create', POST=data)
    def update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_event/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_event/delete', POST={'id': id})
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
