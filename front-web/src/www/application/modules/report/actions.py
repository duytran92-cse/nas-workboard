from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.conf import settings
from django.template import loader
from notasquare.urad_web import actions, widgets, renderers
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from application.modules.board import components as board_components
from application import constants
from . import components, reports

class Summary(common_actions.BaseAction):
    class SummaryWidget(widgets.BaseWidget):
        def __init__(self):
            pass
    class SummaryWidgetRenderer(renderers.BaseRenderer):
        def render(self, summary_widget):
            template = loader.get_template('workboard/report/summary.html')
            context = {}
            context['data'] = summary_widget.data
            return template.render(context)
    def create_summary_widget(self):
        summary_widget = self.SummaryWidget()
        summary_widget.data = components.ReportStore(self.get_container()).get_report_data(self.params['board_id'])['data']['record']
        summary_widget.renderer = self.SummaryWidgetRenderer()
        return summary_widget
    def GET(self):
        page_context = self.create_page_context()
        page_context.add_widget(self.create_summary_widget())
        page_context.page_title = "Summary"
        return HttpResponse(page_context.render())

class ExportPerformanceReport(common_actions.BaseAction):
    def set_color_code(self, pdf, colorcode):
        if colorcode == 'gray':
            pdf.set_text_color(204, 204, 204)
        if colorcode == 'green':
            pdf.set_text_color(0, 100, 0)
        if colorcode == 'red':
            pdf.set_text_color(255, 0, 0)
    def GET(self):
        scoring_schema = constants.SCORING_SCHEMA
        month = self.params.get('month', 0)
        year = self.params.get('year', 0)

        data = components.ReportStore(self.container).get_performance_report_data(month, year)
        performances = data['data']['record']

        builder = reports.MonthlyPerformanceReportBuilder()
        builder.generate_report({
            'year': year,
            'month': month,
            'performances': performances,
            'scoring_schema': scoring_schema,
        }, '/tmp/monthly_performance_report.pdf')

        return FileResponse(open('/tmp/monthly_performance_report.pdf', 'rb'), content_type='application/pdf')

class ExportBoardReport(common_actions.BaseAction):
    def GET(self):
        board_id = self.params.get('board_id', 0)
        board_data = {
            'board': {
                'id': 1,
                'name': 'Board XXX',
                'team': [
                    {'user':  'Vo Anh Quan'},
                    {'user':  'Tran Duc Quang'},
                ],
                'story_stats': {
                    'default':    15,
                    'icebox':     1,
                    'accepted':   5,
                    'failed':     3
                },
                'goal_stats': {
                    'success':    3,
                    'failed':     4,
                    'rejected':   2
                }
            },
            'goals': [
                {
                    'id':     1,
                    'title':  'This is a goal',
                    'user':   'Vo Anh Quan',
                    'status': 'failed',
                },
                {
                    'id':     2,
                    'title':  'This is a goal #2',
                    'user':   'Tran Duc Quang',
                    'status': 'success',
                }
            ],
            'stories': [
                {
                    'category': 'Genome browser',
                    'stories': [
                        {
                            'id':       1,
                            'title':    'This is a story',
                            'user':     'Vo Anh Quan',
                            'category': 'Genome Browser',
                            'status':   'failed',
                        },
                        {
                            'id':       2,
                            'title':    'This is a story',
                            'user':     'Tran Duc Quang',
                            'category': 'Genome Browser',
                            'status':   'accepted',
                        }
                    ]
                }
            ]
        }
        data = components.ReportStore(self.container).get_board_report_data(board_id)
        board_data = data['data']['record']

        builder = reports.BoardReportBuilder()
        builder.generate_report(board_data, '/tmp/board_report.pdf')

        return FileResponse(open('/tmp/board_report.pdf', 'rb'), content_type='application/pdf')
