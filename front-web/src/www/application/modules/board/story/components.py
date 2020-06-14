from django.conf import settings
from django.template import loader
from notasquare.urad_web import actions, widgets, renderers
from application.modules.board.stage import components as board_stage_components
from application.modules.board.category import components as board_category_components
from application.modules.board import components as board_components
from application.common import registry

class BoardStoryStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        if page_number > 0:
            params['_pager_start'] = (page_number - 1) * 10
            params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/get', GET={'id': id})
    def get_logs(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/get_logs', GET={'id': id, 'user_id': registry.USER['user_id']})
    def get_cmts(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/get_cmts', GET={'id': id})
    def get_rating(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/get_rating', GET={'id': id})
    def get_tags(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/get_tags', GET={'id': id})
    def add_cmt(self, data):
        data['user_id'] = registry.USER['user_id']
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/add_cmt', POST=data)
    def add_tag(self, data):
        data['user_id'] = registry.USER['user_id']
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/add_tag', POST=data)
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/create', POST=data)
    def update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/update', POST=data)
    def update_rating(self, data):
        data['user_id'] = registry.USER['user_id']
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/update_rating', POST=data)
    def change_stage(self, data):
        data['user_id'] = registry.USER['user_id']
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/change_stage', POST=data)
    def bulk_delete(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/bulk_delete', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/delete', POST={'id': id})
    def delete_tag(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board_story/delete_tag', POST={'id': id})
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

class StageSideWidget(widgets.BaseWidget):
    def __init__(self):
        pass
    def build(self, container, params):
        self.stage = board_stage_components.BoardStageStore(container).get(params['stage_id'])['data']['record']
        self.renderer = StageSideWidgetRenderer()
class StageSideWidgetRenderer(renderers.BaseRenderer):
    def render(self, stage_side_widget):
        template = loader.get_template('workboard/board/story/stage_side_widget.html')
        context = {}
        context['widget'] = stage_side_widget
        return template.render(context)

class CategorySideWidget(widgets.BaseWidget):
    def __init__(self):
        pass
    def build(self, container, params):
        self.category = board_category_components.BoardCategoryStore(container).get(params['category_id'])['data']['record']
        self.renderer = CategorySideWidgetRenderer()
class CategorySideWidgetRenderer(renderers.BaseRenderer):
    def render(self, category_side_widget):
        template = loader.get_template('workboard/board/story/category_side_widget.html')
        context = {}
        context['widget'] = category_side_widget
        return template.render(context)

class CommentSideWidget(widgets.BaseWidget):
    def __init__(self):
        pass
    def build(self, container, params):
        self.cmts = BoardStoryStore(container).get_cmts(params['id'])['data']['record']
        self.renderer = CommentSideWidgetRenderer()
class CommentSideWidgetRenderer(renderers.BaseRenderer):
    def render(self, comment_side_widget):
        template = loader.get_template('workboard/board/story/comment_side_widget.html')
        context = {}
        context['widget'] = comment_side_widget
        return template.render(context)

class LogSideWidget(widgets.BaseWidget):
    def __init__(self):
        pass
    def build(self, container, params):
        self.logs = BoardStoryStore(container).get_logs(params['id'])['data']['record']
        self.renderer = LogSideWidgetRenderer()
class LogSideWidgetRenderer(renderers.BaseRenderer):
    def render(self, log_side_widget):
        template = loader.get_template('workboard/board/story/log_side_widget.html')
        context = {}
        context['widget'] = log_side_widget
        return template.render(context)

class RatingSideWidget(widgets.BaseWidget):
    def __init__(self):
        pass
    def build(self, container, params):
        self.rating = BoardStoryStore(container).get_rating(params['id'])['data']['record']
        self.renderer = RatingSideWidgetRenderer()
class RatingSideWidgetRenderer(renderers.BaseRenderer):
    def render(self, rating_side_widget):
        template = loader.get_template('workboard/board/story/rating_side_widget.html')
        context = {}
        context['widget'] = rating_side_widget
        return template.render(context)

class TagSideWidget(widgets.BaseWidget):
    def __init__(self):
        pass
    def build(self, container, params):
        self.tags = board_components.BoardStore(container).get_board_tag(params['board_id'])['data']['record']
        self.log_tag = BoardStoryStore(container).get_tags(params['id'])['data']['record']
        self.board_id = params['board_id']
        self.story_id = params['id']
        self.renderer = TagSideWidgetRenderer()
class TagSideWidgetRenderer(renderers.BaseRenderer):
    def render(self, tag_side_widget):
        template = loader.get_template('workboard/board/story/tag_side_widget.html')
        context = {}
        context['widget'] = tag_side_widget
        return template.render(context)

class StoryFormRenderer(renderers.BaseRenderer):
    def __init__(self):
        super(StoryFormRenderer, self).__init__()
        self.form_id = 'form'
        self.field_renderers = {}
    def set_field_renderer(self, code, renderer):
        self.field_renderers[code] = renderer
    def render(self, form):
        template = loader.get_template('workboard/board/story/form.html')
        context = {}
        context['form_id'] = self.form_id
        context['title'] = form.title
        context['messages'] = form.messages
        context['buttons'] = form.buttons

        labels = {
            'name':              'Name',
            'board_category_id': 'Category',
            'board_stage_id':    'Stage',
            'manager_id':        'Manager',
            'assignee_id':          'Assignee',
        }

        field_html = {}
        for id, field in form.fields.iteritems():
            field.label = labels[id] if id in labels else ''
            field_html[id] = self.field_renderers[field.code].render(field, {})
        context['field_html'] = field_html

        return template.render(context)
