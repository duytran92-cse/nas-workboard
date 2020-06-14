
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',                       handlers.Get.as_view(),                         name='board_get'),
    url(r'^get_static$',                handlers.GetStaticNumber.as_view(),             name='board_get'),
    url(r'^get_dashboard$',             handlers.GetDashboard.as_view(),                name='board_get'),
    url(r'^get_home$',                  handlers.GetHome.as_view(),                     name='board_get'),
    url(r'^get_board_tag$',             handlers.GetBoardTag.as_view(),                 name='board_get'),
    url(r'^get_user$',                  handlers.GetAllUser.as_view(),                  name='board_get'),
    url(r'^get_home_static$',           handlers.GetHomeStatistics.as_view(),           name='board_home_static'),
    url(r'^get_summary$',               handlers.GetSummary.as_view(),                  name='board_summary'),
    url(r'^get_cell_assignment$',       handlers.GetCellAssignment.as_view(),           name='board_get_cell_assignment'),
    url(r'^get_board_responsibility$',  handlers.GetBoardResponsibility.as_view(),      name='board_get_board_responsibility'),
    url(r'^get_board_report$',          handlers.GetReport.as_view(),                   name='board_get_board_report'),
    url(r'^get_performance_report_data$', handlers.GetPerformanceReportData.as_view(),  name='board_get_performance_report_data'),
    url(r'^get_board_report_data$',     handlers.GetBoardReportData.as_view(),          name='board_get_board_report_data'),
    url(r'^list$',                      handlers.List.as_view(),                        name='board_list'),
    url(r'^create$',                    handlers.Create.as_view(),                      name='board_create'),
    url(r'^update$',                    handlers.Update.as_view(),                      name='board_update'),
    url(r'^delete$',                    handlers.Delete.as_view(),                      name='board_delete'),
    url(r'^duplicate$',                 handlers.Duplicate.as_view(),                   name='board_duplicate'),
]
