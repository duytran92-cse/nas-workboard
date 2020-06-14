from django.contrib.humanize.templatetags.humanize import naturaltime
from notasquare.urad_api import *
from application.models import *
from application import constants
from django.db.models import Q, Count
from datetime import datetime
from application.modules.common import helpers

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = Queue.objects
        if data.get('text', '') != '' :
            query = query.filter(name__contains=data['text'])
        return query
    def serialize_entry(self, queue):
        return {
            'id':               queue.id,
            'name':             queue.name,
            'description':      queue.description,
            'text_color':       queue.text_color,
            'bg_color':         queue.bg_color
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        queue = Queue.objects.get(pk=data['id'])

        return {
            'id':               queue.id,
            'name':             queue.name,
            'description':      queue.description,
            'text_color':       queue.text_color,
            'bg_color':         queue.bg_color
        }

class Create(handlers.standard.CreateHandler):
    def create(self, data):
        queue = Queue()
        queue.name = data.get('name', '')
        queue.description = data.get('description', '')
        queue.text_color = data.get('text_color', '')
        queue.bg_color = data.get('bg_color', '')
        queue.save()

        return queue


class Update(handlers.standard.UpdateHandler):
    def update(self, data):
        queue = Queue.objects.get(pk=data['id'])
        if data.get('name', ''):
            queue.name = data.get('name', '')
        if data.get('description', ''):
            queue.description = data.get('description', '')
        if data.get('text_color', ''):
            queue.text_color = data.get('text_color', '')
        if data.get('bg_color', ''):
            queue.bg_color = data.get('bg_color', '')
        queue.save()
        return queue

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        queue = Queue.objects.get(pk=data['id'])
        queue.delete()
        return 1
