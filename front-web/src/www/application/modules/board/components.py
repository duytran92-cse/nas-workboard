from django.conf import settings
from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer

from application.modules.common import page_contexts
from application.modules.board.stage import components as board_stage_components
from application.modules.board.category import components as board_category_components
from django.conf import settings
from application.common import registry


class BoardStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        params['front'] = 'no_template_boards'
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/board/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get', GET={'id': id})
    def get_dashboard(self):
        params = {
            'user_id': registry.USER['user_id']
        }
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_dashboard', GET=params)
    def get_home(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_home', GET={'id': id, 'user_id': registry.USER['user_id']})
    def get_board_tag(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_board_tag', GET={'id': id, 'user_id': registry.USER['user_id']})
    def get_home_static(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_home_static', GET={'id': id, 'user_id': registry.USER['user_id']})
    def get_number_static(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_static', GET={'id': id, 'user_id': registry.USER['user_id']})
    def get_cell_assignment(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_cell_assignment', GET={'id': id})
    def get_board_responsibility(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_board_responsibility', GET={'id': id})
    def get_summary(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_summary', GET={'id': id})
    def get_user_assignee(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_user', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/create', POST=data)
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

class BoardFullPageContextRenderer(BaseRenderer):
    def __init__(self):
        super(BoardFullPageContextRenderer, self).__init__()
        self.template = 'workboard/page_contexts/full.html'
    def render(self, full_page_context):
        template = loader.get_template(self.template)
        context = {}
        context['page_title'] = full_page_context.page_title
        context['context'] = full_page_context
        context['user'] = full_page_context.user

        widget_html = ''
        for widget in full_page_context.widgets:
            widget_html += widget.render()
        context['widget_html'] = widget_html

        side_widget_html = ''
        for widget in full_page_context.side_widgets:
            side_widget_html += widget.render()
        context['side_widget_html'] = side_widget_html
        return template.render(context)

class BoardFullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(BoardFullPageContext, self).__init__()
        self.renderer = BoardFullPageContextRenderer()
        self.renderer.template = 'workboard/board/page_contexts.html'

        self.side_widgets = []

        self.board_id = params['board_id']
        self.menu = params['submenu']
        self.page_title = params['page_title']
        self.board = BoardStore(container).get(params['board_id'])['data']['record']
        self.stages = board_stage_components.BoardStageStore(container).list({'board_id': params['board_id']}, sortkey='sort_order', sortdir='asc', page_number=0)['records']
        self.categories = board_category_components.BoardCategoryStore(container).list({'board_id': params['board_id']})['records']
        self.user_assignee = BoardStore(container).get_user_assignee(params['board_id'])['data']['record']
        self.num_static = BoardStore(container).get_number_static(params['board_id'])['data']['record']

        # User
        self.user = registry.USER
        self.user['logout_link'] = settings.SECURITY_SERVER_URL + '/user/logout?redirect=%s' % (settings.APPLICATION_URL)

    def add_side_widget(self, widget):
        self.side_widgets.append(widget)
