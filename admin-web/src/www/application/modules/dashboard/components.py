from django.conf import settings
from application.modules.common import page_contexts
from django.template import loader
from django.conf import settings
from application.common import registry

class PageFullPageContext(page_contexts.FullPageContext):
    def __init__(self, params):
        super(PageFullPageContext, self).__init__()
        self.template = 'material/page_contexts/full.html'

        self.page_title = 'Dashboard'
        self.menu.set_group_selected('dashboard')
        self.breadcrumb.add_entry('dashboard', 'Dashboard', '/dashboard/view')

        # User
        self.user = registry.USER
        self.user['logout_link'] = settings.SECURITY_SERVER_URL + '/user/logout?redirect=%s' % (settings.APPLICATION_URL)

    def render(self, full_page_context):
        template = loader.get_template(self.template)
        context = {
            'app_title':      full_page_context.app_title,
            'page_title':     full_page_context.page_title,
            'menu':           full_page_context.menu,
            'submenu':        full_page_context.submenu,
            'breadcrumb':     full_page_context.breadcrumb,
            'user':           full_page_context.user
        }
        context['widget_html'] = 'Welcome to workboard administration panel!'
        return template.render(context)
