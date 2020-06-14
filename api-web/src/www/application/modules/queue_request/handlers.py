from django.contrib.humanize.templatetags.humanize import naturaltime
from notasquare.urad_api import *
from application.models import *
from application import constants

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = QueueRequest.objects
        queue_id = data.get('queue_id', 0)
        query = query.filter(queue_id=queue_id)
        if data.get('text', '') != '' :
            query = query.filter(name__contains=data['text'])
        if data.get('board_id', '') != '':
            query = query.filter(board_id=data.get('board_id'))
        else:
            query = query.filter(board_id=None)

        return query
    def serialize_entry(self, queue_request):
        return {
            'id':               queue_request.id,
            'queue_id':         queue_request.queue_id,
            'title':            queue_request.title,
            'description':      queue_request.description,
            'requestor_id':     queue_request.requestor_id,
            'requestor_label':  queue_request.requestor.name if queue_request.requestor else '',
            'timestamp':        queue_request.timestamp,
            'priority':         queue_request.priority,
            'priority_label':   queue_request.priority,
            'deadline':         queue_request.deadline if queue_request.deadline else '',
            'status':           queue_request.status,
            'status_label':     queue_request.status,
        }



class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        queue_request = QueueRequest.objects.get(pk=data['id'])

        return {
            'id':               queue_request.id,
            'queue_id':         queue_request.queue_id,
            'title':            queue_request.title,
            'description':      queue_request.description,
            'requestor_id':     queue_request.requestor_id,
            'requestor_label':  queue_request.requestor.name if queue_request.requestor else '',
            'timestamp':        queue_request.timestamp,
            'priority':         queue_request.priority,
            'priority_label':   queue_request.priority,
            'deadline':         queue_request.deadline if queue_request.deadline else '',
            'status':           queue_request.status,
            'status_label':     queue_request.status,
        }


class Create(handlers.standard.CreateHandler):
    def create(self, data):
        request = QueueRequest()
        request.queue_id = data.get('queue_id', 0)
        request.title = data.get('title', '')
        request.description = data.get('description', '')
        if data.get('requestor_id', '') != '':
            request.requestor_id = data.get('requestor_id')
        if data.get('priority', '') != '':
            request.priority = data.get('priority')
        if data.get('deadline', '') != '':
            request.deadline = data.get('deadline')
        if data.get('status', '') != '':
            request.status = data.get('status')
        request.save()
        return request


class Update(handlers.standard.UpdateHandler):
    def update(self, data):
        request = QueueRequest.objects.get(pk=data['id'])
        if data.get('title', '') != '':
            request.title = data.get('title', '')
        if data.get('description', '') != '':
            request.description = data.get('description', '')
        if data.get('requestor_id', '') != '':
            request.requestor_id = data.get('requestor_id')
        if data.get('priority', '') != '':
            request.priority = data.get('priority')
        if data.get('deadline', '') != '':
            request.deadline = data.get('deadline')
        if data.get('status', '') != '':
            request.status = data.get('status')
        request.save()
        return request

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        request = QueueRequest.objects.get(pk=data['id'])
        request.delete()
        return 1
