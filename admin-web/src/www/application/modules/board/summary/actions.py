from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import loader
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from notasquare.urad_web.renderers import BaseRenderer
from application import constants
from . import components
from application.modules.board import components as board_components

class Summary(actions.crud.FormAction):
    def create_page_context(self):
        self.params['submenu'] = "summary"
        return board_components.BoardFullPageContext(self.params, self.container)
    class SummaryRenderer(BaseRenderer):
        def render(self, table):
            template = loader.get_template('material/summary/summary.html')
            context = {}
            context['summary'] = table.data
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.SummaryRenderer()
        return table
    def load_table_data(self):
        return board_components.BoardStore(self.get_container()).get_summary(self.params['board_id'])
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data = data['data']['record']
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())
