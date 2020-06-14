from django.conf import settings

class ReportStore(object):
    def __init__(self, container):
        self.container = container
    def get_report_data(self, id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_board_report', GET={'id': id})
    def get_performance_report_data(self, month, year):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_performance_report_data', GET={'month': month, 'year': year})
    def get_board_report_data(self, board_id):
        return self.container.call_api(settings.WORKBOARD_API_URL + '/board/get_board_report_data', GET={'board_id': board_id})
