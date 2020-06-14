from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import loader
from notasquare.urad_web import actions, widgets, renderers
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from application.modules.statistics import components as statistics_components
from application import constants
from . import components
from application.common import registry
from collections import OrderedDict
import json

class Home(common_actions.BaseAction):
    class HomeWidget(widgets.BaseWidget):
        def __init__(self):
            pass
    class HomeWidgetRenderer(renderers.BaseRenderer):
        def render(self, home_widget):
            template = loader.get_template('workboard/statistics/home.html')
            context = {}
           
            context['board_statistics'] = home_widget.board_statistics_data

            context['board_open'] = []
            context['board_in_progress'] = []
            context['board_completed'] = []
            context['board_closed'] = []

            context['board_status'] = []

            for sts in context['board_statistics'].get('data').get('record').get('status').get('status'):
            	context['board_status'].append({
            		'sts': sts.values()[0],
            		'bg_color': sts.values()[1],
            		'text_color': sts.values()[3],
            		'total': sts.values()[2],
            	})

            for b in context['board_statistics'].get('data').get('record').get('result').get('open').get('data'):
            	context['board_open'].append({
                    'board': b.values()[1],
                })
            	print b.values()[1]
            
            for b in context['board_statistics'].get('data').get('record').get('result').get('in_progress').get('data'):
                context['board_in_progress'].append({
                    'board': b.values()[1],
                })

            for b in context['board_statistics'].get('data').get('record').get('result').get('completed').get('data'):
                context['board_completed'].append({
                    'board': b.values()[1],
                })

            for b in context['board_statistics'].get('data').get('record').get('result').get('closed').get('data'):
                context['board_closed'].append({
                    'board': b.values()[1],
                })

            # #---------------------------------------------------

            context['user_statistics'] = home_widget.user_statistics_data

            context['total_user'] = context['user_statistics'].get('data').get('record').get('number_user')
            
            context['user_data'] = []

            for user in context['user_statistics'].get('data').get('record').get('data'):
                context['user_data'].append({
                    'user': user.keys()[0],
                    'stories_backlog':user.values()[0].get('stories_backlog'),
                    'stories_pending':user.values()[0].get('stories_pending'),
                    'stories_in_progress': user.values()[0].get('stories_in_progress'),
                    'stories_acceptance':user.values()[0].get('stories_acceptance'),
                    'stories_accepted':user.values()[0].get('stories_accepted'),
                    'stories_testinh':user.values()[0].get('stories_testing'),
                    'stories_icebox':user.values()[0].get('stories_icebox'),
                    'stories_failed':user.values()[0].get('stories_failed'),
                    'total_stories': len(user.values()[0].get('stories_backlog')) + len(user.values()[0].get('stories_pending')) + len(user.values()[0].get('stories_in_progress')) + len(user.values()[0].get('stories_acceptance')) + len(user.values()[0].get('stories_accepted')) + len(user.values()[0].get('stories_testing')) + len(user.values()[0].get('stories_icebox')) + len(user.values()[0].get('stories_failed')),
                })


            
            context['story_in_progress'] = home_widget.story_in_progress_data.get('data').get('record').get('num_stories')
            # print context['story_in_progress_data'].get('data').get('record').get('num_stories')
            
            context['user'] = registry.USER
            return template.render(context)

    def create_home_widget(self):
        home_widget = self.HomeWidget()

        home_widget.story_in_progress_data = statistics_components.StatisticsStore(self.get_container()).get_story_in_progress()
        home_widget.user_statistics_data =  statistics_components.StatisticsStore(self.get_container()).get_user_statistics()
        home_widget.board_statistics_data = statistics_components.StatisticsStore(self.get_container()).get_board_statistics()
        

        home_widget.renderer = self.HomeWidgetRenderer()
        return home_widget

    def GET(self):
        page_context = self.create_page_context()
        page_context.add_widget(self.create_home_widget())
        page_context.page_title = "Dashboard"
        return HttpResponse(page_context.render())
