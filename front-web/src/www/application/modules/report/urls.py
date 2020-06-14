
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^(?P<board_id>([0-9]+))$',           actions.Summary.as_view(),                    name='summary_view'),
    url(r'export_performance_report$',         actions.ExportPerformanceReport.as_view(),    name='export_performance_report'),
    url(r'export_board_report$',               actions.ExportBoardReport.as_view(),          name='export_board_report'),
]
