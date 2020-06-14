from django.conf import settings
from django.template import loader
from notasquare.urad_web import actions, widgets, renderers
from application.modules.board.stage import components as board_stage_components
from application.modules.board.category import components as board_category_components
from application.common import registry

class QueueRequestStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        if page_number > 0:
            params['_pager_start'] = (page_number - 1) * 10
            params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/queue_request/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue_request/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue_request/create', POST=data)
    def update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue_request/update', POST=data)
    def bulk_delete(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue_request/bulk_delete', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/queue_request/delete', POST={'id': id})

class RequestFormRenderer(renderers.BaseRenderer):
    def __init__(self):
        super(RequestFormRenderer, self).__init__()
        self.form_id = 'form'
        self.field_renderers = {}
    def set_field_renderer(self, code, renderer):
        self.field_renderers[code] = renderer
    def render(self, form):
        template = loader.get_template('workboard/queue/request/form.html')
        context = {}
        context['form_id'] = self.form_id
        context['title'] = form.title
        context['messages'] = form.messages
        context['buttons'] = form.buttons

        labels = {
            'title':              'Title',
            'description':        'Description',
            'requestor_id':       'Requestor',
            'deadline':           'Deadline',
            'priority':           'Priority',
            'status':             'Status',
        }

        field_html = {}
        for id, field in form.fields.iteritems():
            field.label = labels[id] if id in labels else ''
            field_html[id] = self.field_renderers[field.code].render(field, {})
        context['field_html'] = field_html

        return template.render(context)
