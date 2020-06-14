from notasquare.urad_web.page_contexts import standard
from notasquare.urad_web_material import renderers
from django.conf import settings
from application.common import registry

class FullPageContext(standard.FullPageContext):
    def __init__(self):
        super(FullPageContext, self).__init__()
        self.app_title = 'Workboard'
        self.page_title = 'Workboard'
        self.menu.create_menu_group('dashboard', 'Dashboard', '/', 'zmdi-format-subject')
        self.menu.create_menu_group('queue', 'Queue', '/queue/list', 'zmdi-format-subject')
        self.menu.create_menu_group('board', 'Board', '/board/list', 'zmdi-format-subject')
        self.menu.create_menu_group('user', 'User', '/user/list', 'zmdi-format-subject')
        self.menu.create_menu_group('user_monthly_performance', 'Monthly Performance', '/user_monthly_performance/list', 'zmdi-format-subject')
        self.renderer = renderers.page_contexts.FullPageContextRenderer()

        # User
        self.user = registry.USER
        self.user['logout_link'] = settings.SECURITY_SERVER_URL + '/user/logout?redirect=%s' % (settings.APPLICATION_URL)
