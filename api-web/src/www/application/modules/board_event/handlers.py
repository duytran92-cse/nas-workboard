from django.contrib.humanize.templatetags.humanize import naturaltime
from notasquare.urad_api import *
from application.models import *
from application import constants

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = BoardEvent.objects
        board_id = data.get('board_id', 0)
        query = query.filter(board_id=board_id)
        if data.get('text', '') != '' :
            query = query.filter(name__contains=data['text'])
        return query
    def serialize_entry(self, board_event):
        return {
            'id':               board_event.id,
            'board_id':         board_event.board_id,
            'event_date':       board_event.event_date,
            'name':             board_event.name,
        }



class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        board_event = BoardEvent.objects.get(pk=data['id'])

        return {
            'id':               board_event.id,
            'board_id':         board_event.board_id,
            'event_date':       board_event.event_date,
            'name':             board_event.name,
        }


class Create(handlers.standard.CreateHandler):
    def create(self, data):
        event = BoardEvent()
        event.board_id = data.get('board_id', 0)
        if data.get('event_date', ''):
            event.event_date = data.get('event_date','')
        if data.get('name', ''):
            event.name = data.get('name', '')
        event.save()
        return event


class Update(handlers.standard.UpdateHandler):
    def update(self, data):
        event = BoardEvent.objects.get(pk=data['id'])
        if data.get('event_date', ''):
            event.event_date = data.get('event_date', '')
        if data.get('name', ''):
            event.name = data.get('name', '')
        event.save()
        return event

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        event = BoardEvent.objects.get(pk=data['id'])
        event.delete()
        return 1
