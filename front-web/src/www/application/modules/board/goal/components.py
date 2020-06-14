from django.conf import settings
from django.template import loader
from notasquare.urad_web import actions, widgets, renderers
from application.common import registry

class BoardGoalStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        if page_number > 0:
            params['_pager_start'] = (page_number - 1) * 10
            params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/board_goal/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_goal/get', GET={'id': id})
    def get_bulk_update(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_goal/get_bulk_update', GET={'board_id': id})
    def bulk_update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_goal/bulk_update', POST=data)
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_goal/create', POST=data)
    def update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_goal/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_goal/delete', POST={'id': id})
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

class BoardGoalFormRenderer(renderers.BaseRenderer):
    def __init__(self):
        super(BoardGoalFormRenderer, self).__init__()
        self.form_id = 'form'
        self.field_renderers = {}
    def set_field_renderer(self, code, renderer):
        self.field_renderers[code] = renderer
    def render(self, form):
        template = loader.get_template('workboard/board/goal/form.html')
        context = {}
        context['form_id'] = self.form_id
        context['title'] = form.title
        context['messages'] = form.messages
        context['buttons'] = form.buttons

        labels = {
            'name':              'Name',
            'user_id':              'User',
            'description': '',
            'status':    'Status',
            'objectives':          'Objectives',
        }

        field_html = {}
        for id, field in form.fields.iteritems():
            field.label = labels[id] if id in labels else ''
            if id == 'objectives':
                field_html[id] = self.field_renderers[field.code].render(field, {
                    'columns': [
                        {'id': 'result',            'label': 'Result',             'width': '10%'},
                        {'id': 'description',         'label': 'Description',             'width': '30%'},
                        {'id': 'note',     'label': 'Note',      'width': '40%'},
                    ]
                })
            else:
                field_html[id] = self.field_renderers[field.code].render(field, {})

        context['field_html'] = field_html

        return template.render(context)

