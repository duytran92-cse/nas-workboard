from django.contrib.humanize.templatetags.humanize import naturaltime
from notasquare.urad_api import *
from application.models import *
from application import constants

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = User.objects
        if data.get('text', '') != '' :
            query = query.filter(name__contains=data['text'])
        return query
    def serialize_entry(self, user):
        return {
            'id':               user.id,
            'username':         user.username,
            'name':             user.name,
        }



class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        user = User.objects.get(pk=data['id'])
        return {
            'id':         user.id,
            'username':   user.username,
            'name':       user.name
        }

class GetByUsername(handlers.standard.GetHandler):
    def get_data(self, data):
        try:
            user = User.objects.filter(username=data['username']).first()
            return {
                'id': user.id,
                'name': user.name
            }
        except e:
            return {'id': 0}

class Create(handlers.standard.CreateHandler):
    def create(self, data):
        user = User()
        user.username = data['username']
        user.name = data['name']
        user.save()
        return user


class Update(handlers.standard.UpdateHandler):
    def update(self, data):
        user = User.objects.get(pk=data['id'])
        if data.get('username', ''):
            user.username = data.get('username')
        if data.get('name', ''):
            user.name = data.get('name')
        user.save()
        return user

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        user = User.objects.get(pk=data['id'])
        user.delete()
        return 1
