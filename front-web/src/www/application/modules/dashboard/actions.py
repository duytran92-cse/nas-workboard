from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import loader
from notasquare.urad_web import actions, widgets, renderers
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from application.modules.board import components as board_components
from application import constants
from . import components
from application.common import registry

class Home(common_actions.BaseAction):
    class HomeWidget(widgets.BaseWidget):
        def __init__(self):
            pass
    class HomeWidgetRenderer(renderers.BaseRenderer):
        def render(self, home_widget):
            template = loader.get_template('workboard/dashboard/home.html')
            context = {}
            context['dashboard_data'] = home_widget.dashboard_data
            context['user'] = registry.USER

            return template.render(context)
    def create_home_widget(self):
        home_widget = self.HomeWidget()
        home_widget.dashboard_data = board_components.BoardStore(self.get_container()).get_dashboard()['data']['record']
        home_widget.renderer = self.HomeWidgetRenderer()
        return home_widget
        
    def GET(self):
        page_context = self.create_page_context()
        page_context.add_widget(self.create_home_widget())
        page_context.page_title = "Dashboard"
        return HttpResponse(page_context.render())
