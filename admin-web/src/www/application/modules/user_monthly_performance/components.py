from django.conf import settings
from application.modules.common import page_contexts

class UserMonthlyPerformanceStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=0):
        if page_number > 0:
            params['_pager_start'] = (page_number - 1) * 10
            params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.WORKBOARD_API_URL + '/user_monthly_performance/list', GET=params)
        return data['data']
    def get(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/user_monthly_performance/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/user_monthly_performance/create', POST=data)
    def update(self, data):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/user_monthly_performance/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/user_monthly_performance/delete', POST={'user_id': id})

class UserMonthlyPerformanceFullPageContext(page_contexts.FullPageContext):
    def __init__(self, params, container):
        super(UserMonthlyPerformanceFullPageContext, self).__init__()
        self.page_title = 'User monthly performance'
        self.menu.set_group_selected('user_monthly_performance')

        self.breadcrumb.add_entry('user_monthly_performance', 'User Monthly Performance', '/user_monthly_performance/list')
