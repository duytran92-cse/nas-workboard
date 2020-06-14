from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import loader
from notasquare.urad_web import actions, widgets, renderers
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from application.modules.board.stage import components as board_stage_components
from application.modules.board.category import components as board_category_components
from application import constants
from . import components
from application.common import registry

class Home(common_actions.BaseAction):
    class HomeWidget(widgets.BaseWidget):
        def __init__(self):
            pass
    class HomeWidgetRenderer(renderers.BaseRenderer):
        def render(self, home_widget):
            template = loader.get_template('workboard/board/home.html')
            context = {}
            context['board'] =              home_widget.board
            context['num_static'] =         home_widget.num_static
            context['stages'] =             home_widget.stages
            context['categories'] =         home_widget.categories
            context['user_assignee'] =      home_widget.user_assignee
            context['home_data'] =          home_widget.home_data
            context['home_static'] =        home_widget.home_static
            context['user']=                registry.USER
            return template.render(context)
    def create_home_widget(self):
        home_widget = self.HomeWidget()
        board = components.BoardStore(self.get_container()).get(self.params['board_id'])
        home_widget.board = board['data']['record']
        home_widget.num_static = components.BoardStore(self.get_container()).get_number_static(self.params['board_id'])['data']['record']
        home_widget.stages = board_stage_components.BoardStageStore(self.get_container()).list({'board_id': self.params['board_id']}, sortkey='sort_order', sortdir='asc', page_number=0)['records']
        home_widget.categories = board_category_components.BoardCategoryStore(self.get_container()).list({'board_id': self.params['board_id']})['records']
        home_widget.home_data = components.BoardStore(self.get_container()).get_home(self.params['board_id'])['data']['record']
        home_widget.user_assignee = components.BoardStore(self.get_container()).get_user_assignee(self.params['board_id'])['data']['record']
        home_widget.home_static = components.BoardStore(self.get_container()).get_home_static(self.params['board_id'])['data']['record']
        home_widget.renderer = self.HomeWidgetRenderer()
        return home_widget
    def GET(self):
        page_context = self.create_page_context()
        page_context.add_widget(self.create_home_widget())
        page_context.page_title = "Home"
        return HttpResponse(page_context.render())

class ViewAssignment(common_actions.BaseAction):
    def create_page_context(self):
        self.params['submenu'] = 'assignment'
        self.params['page_title'] = 'Instruction'
        return components.BoardFullPageContext(self.params, self.container)
    class ViewAssignmentWidget(widgets.BaseWidget):
        def __init__(self):
            pass
    class ViewAssignmentWidgetRenderer(renderers.BaseRenderer):
        def render(self, view_assignment_widget):
            template = loader.get_template('workboard/board/view_assignment.html')
            context = {}
            context['widget'] = view_assignment_widget
            return template.render(context)
    def create_view_assignment_widget(self):
        view_assignment_widget = self.ViewAssignmentWidget()
        view_assignment_widget.renderer = self.ViewAssignmentWidgetRenderer()

        view_assignment_widget.stages = board_stage_components.BoardStageStore(self.container).list({'board_id': self.params['board_id']}, sortkey='id', sortdir='asc')['records']

        categories = board_category_components.BoardCategoryStore(self.container).list({'board_id': self.params['board_id']})['records']
        cell_assignments = components.BoardStore(self.container).get_cell_assignment(self.params['board_id'])['data']['record']
        board_responsibility = components.BoardStore(self.container).get_board_responsibility(self.params['board_id'])['data']['record']
        for c in categories:
            c['assignments'] = []
            for s in view_assignment_widget.stages:
                c['assignments'].append(cell_assignments["%s-%s" % (s['id'], c['id'])])

        view_assignment_widget.categories = categories
        view_assignment_widget.board_responsibility = board_responsibility

        return view_assignment_widget
    def GET(self):
        page_context = self.create_page_context()
        page_context.add_widget(self.create_view_assignment_widget())
        page_context.page_title = "Board - Assignment"
        return HttpResponse(page_context.render())
