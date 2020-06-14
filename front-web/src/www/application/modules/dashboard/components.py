from django.conf import settings

class DashboardStore(object):
    def __init__(self, container):
        self.container = container
