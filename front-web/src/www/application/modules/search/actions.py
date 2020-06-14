from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import loader
from notasquare.urad_web import actions, widgets, renderers
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from application.modules.search import components as search_components
from application import constants
from . import components
from application.common import registry

class Search(common_actions.BaseAction):
    class SearchWidget(widgets.BaseWidget):
        def __init__(self):
            pass

    class SearchWidgetRenderer(renderers.BaseRenderer):
        def render(self, search_widget):
            template = loader.get_template('workboard/search/search.html')
            context = {}
            context['search_data'] = search_widget.search_data
            print context['search_data']

            context['keyword'] = search_widget.keyword
            context['user'] = registry.USER
            return template.render(context)

    def create_search_widget(self):
        search_widget = self.SearchWidget()
        search_widget.search_data = search_components.SearchStore(self.get_container()).get_search(self.params['keyword'])
        search_widget.keyword = self.params['keyword']
        search_widget.renderer = self.SearchWidgetRenderer()
        return search_widget
        
    def GET(self):
        page_context = self.create_page_context()
        page_context.add_widget(self.create_search_widget())
        page_context.page_title = "Search"
        return HttpResponse(page_context.render())
