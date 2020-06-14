from notasquare.urad_web.page_contexts import standard
from application.themes.workboard import renderers
from application.modules.common import components as common_components
from django.conf import settings
from application.common import registry


class FullPageContext(standard.FullPageContext):
    def __init__(self):
        super(FullPageContext, self).__init__()
        self.page_title = 'Workboard'
        self.page_title = 'Workboard'
        #self.menu.create_menu_group('variation', 'Variation', '/variation/list', 'zmdi-format-subject')
        #self.menu.create_menu_group('gene', 'Gene', '/gene/list', 'zmdi-format-subject')
        #self.menu.create_menu_group('disease', 'Disease', '/disease/list', 'zmdi-format-subject')
        self.renderer = renderers.page_contexts.FullPageContextRenderer()

        self.session = ''
        self.messages = None
        # User
        self.user = registry.USER
        self.user['logout_link'] = settings.SECURITY_SERVER_URL + '/user/logout?redirect=%s' % (settings.APPLICATION_URL)
