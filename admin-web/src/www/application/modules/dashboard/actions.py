from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from . import components

class Dashboard(actions.crud.BaseAction):
    def create_page_context(self):
        return components.PageFullPageContext(self.params)
    def GET(self):
        page_context = self.create_page_context()
        return HttpResponse(page_context.render(page_context))
