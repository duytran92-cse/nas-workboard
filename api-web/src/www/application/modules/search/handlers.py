from notasquare.urad_api import *
from application.models import *
from application import constants
from django.conf import settings
from django.db.models import Q

class Search(handlers.standard.GetHandler):
	def get_data(self, data):

		kw=str(data['keyword'])

		result = {
			'board': [],
			'category': [],
			'story': [],
			'matches': 0,
		}
		
		for board in Board.objects.filter(name__icontains=kw):
			record = {'name': board.name, 'id': board.id}
			result['board'].append(record)

		for category in BoardCategory.objects.filter(name__icontains=kw):
			record = {'name': category.name, 'board_id': category.board.id, 'category_id': category.id}
			result['category'].append(record)

		for story in BoardStory.objects.filter(name__icontains=kw):
			record = {'name': story.name, 'board_id': story.board.id, 'story_id': story.id}
			result['story'].append(record)

		result['matches'] = len(result['board']) + len(result['category']) + len(result['story']) 

		return result