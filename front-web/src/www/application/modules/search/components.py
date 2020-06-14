from django.conf import settings

class SearchStore(object):
	def __init__(self, container):
		self.container = container
	def get_search(self, params):
		data = self.container.call_api(settings.WORKBOARD_API_URL + '/search/', GET={'keyword': params})
		return data['data']['record']