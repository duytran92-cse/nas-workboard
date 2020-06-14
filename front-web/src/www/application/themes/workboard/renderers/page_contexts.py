from django.template import loader
from django.conf import settings
from notasquare.urad_web.renderers import BaseRenderer
from application.common import registry

class FullPageContextRenderer(BaseRenderer):
    def __init__(self):
        super(FullPageContextRenderer, self).__init__()
        self.template = 'workboard/page_contexts/full.html'
    def render(self, full_page_context):
        template = loader.get_template(self.template)
        context = {}
        context['page_title'] = full_page_context.page_title
        context['page_title'] = full_page_context.page_title
        context['context'] = full_page_context
        context['user'] = registry.USER

        widget_html = ''
        for widget in full_page_context.widgets:
            widget_html += widget.render()
        context['widget_html'] = widget_html
        return template.render(context)
