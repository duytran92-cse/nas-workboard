from django.conf import settings
from application.modules.common import page_contexts

class BoardSummaryStore(object):
    def __init__(self, container):
        self.container = container

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
