from django.conf import settings
from application.modules.common import page_contexts

class BoardStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/board/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get', GET={'id': id})
    def get_summary(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_summary', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/create', POST=data)
    def duplicate(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/duplicate', POST=data)
    def update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/delete', POST={'id': id})
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


class BoardFullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(BoardFullPageContext, self).__init__()
        self.page_title = 'Board'
        self.menu.set_group_selected('board')

        self.breadcrumb.add_entry('board', 'Board', '/board/list')
        if 'board_id' in params and params['board_id']:
            self.submenu.create_menu_group('summary', 'Summary', '/board/summary/%s' % (str(params['board_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('update', 'Board', '/board/update/%s' % (str(params['board_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('goal', 'Goal', '/board/detail/%s/goal/list' % (str(params['board_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('stage', 'Stage', '/board/detail/%s/stage/list' % (str(params['board_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('category', 'Category', '/board/detail/%s/category/list' % (str(params['board_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('task', 'Task', '/board/detail/%s/task/list' % (str(params['board_id'])), 'zmdi-border-all')
            self.submenu.create_menu_group('tag', 'Tag', '/board/detail/%s/tag/list' % (str(params['board_id'])), 'zmdi-border-all')
            self.submenu.set_group_selected(params['submenu'])
