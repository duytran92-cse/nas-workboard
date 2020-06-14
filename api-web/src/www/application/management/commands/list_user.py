from application.models import *
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		for data in BoardStage.objects.filter(name='Backlog'):
			for i in data.description:
				print i.items()
					