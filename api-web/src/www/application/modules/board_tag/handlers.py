from django.contrib.humanize.templatetags.humanize import naturaltime
from notasquare.urad_api import *
from application.models import *
from application import constants
from application.modules.common import helpers



class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = BoardTag.objects
        board_id = data.get('board_id', 0)
        query = query.filter(board_id=board_id)
        if data.get('text', '') != '' :
            query = query.filter(name__contains=data['text'])
        return query
    def serialize_entry(self, board_tag):
        return  {
            'id':             board_tag.id,
            'board_id':       board_tag.board_id,
            'name':           board_tag.name,
            'icon':           board_tag.icon,
            'is_visible':     board_tag.is_visible
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        board_tag = BoardTag.objects.get(pk=data['id'])
        return {
            'id':             board_tag.id,
            'board_id':       board_tag.board_id,
            'name':           board_tag.name,
            'icon':           board_tag.icon,
            'is_visible':     board_tag.is_visible
        }

class Create(handlers.standard.CreateHandler):
    def create(self, data):
        tag = BoardTag()
        tag.board_id = data.get('board_id', 0)
        if data.get('name', ''):
            tag.name = data.get('name', '')
        if data.get('icon', 'zmdi zmdi-more'):
            tag.icon = data.get('icon', 'zmdi zmdi-more')
        if data.get('is_visible', True):
            tag.is_visible = data.get('is_visible', True)
        tag.save()
        return tag


class Update(handlers.standard.UpdateHandler):
    def update(self, data):
        tag = BoardTag.objects.get(pk=data['id'])
        if data.get('name', ''):
            tag.name = data.get('name', '')
        if data.get('icon', 'zmdi zmdi-more'):
            tag.icon = data.get('icon', 'zmdi zmdi-more')
        if data.get('is_visible', True):
            tag.is_visible = data.get('is_visible', True)
        tag.save()
        return tag

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        tag = BoardTag.objects.get(pk=data['id'])
        tag.delete()
        return 1
