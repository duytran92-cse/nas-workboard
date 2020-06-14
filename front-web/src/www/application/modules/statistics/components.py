from django.conf import settings
from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer
from application.modules.common import page_contexts


from django.conf import settings
from application.common import registry
#--> call to api

class StatisticsStore(object):
	def __init__(self, container):
		self.container = container

	def get_board_statistics(self):
		return self.container.call_api(settings.WORKBOARD_API_URL + '/statistics/board_statistics')	#--> number of board in progress

	def get_story_in_progress(self):
		return self.container.call_api(settings.WORKBOARD_API_URL + '/statistics/story_in_progress')	#--> number of story in progress

	def get_user_statistics(self):
		return self.container.call_api(settings.WORKBOARD_API_URL + '/statistics/user_statistics')	#--> number of story in progress
