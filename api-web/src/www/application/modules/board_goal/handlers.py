from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Count
from notasquare.urad_api import *
from application.models import *
from application import constants



class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = BoardGoal.objects
        board_id = data.get('board_id', 0)
        query = query.filter(board_id=board_id)
        if data.get('text', '') != '' :
            query = query.filter(name__contains=data['text'])
        if data.get('user_id', 0) != 0:
            query = query.filter(user_id=data.get('user_id'))
        return query
    def serialize_entry(self, board_goal):
        objectives = list(board_goal.boardgoalobjectives_set.values('result').annotate(count=Count('result')).order_by('count'))
        objs = []
        for objective in objectives:
            record = constants.OBJECTIVE_RESULTS_DATA.get(objective.get('result'))
            record['count'] = objective.get('count')
            objs.append(record)
        status = constants.BOARD_GOAL_STATUS_DATA.get(board_goal.status)
        return {
            'id':                     board_goal.id,
            'board_id':               board_goal.board_id,
            'name':                   board_goal.name,
            'description':            board_goal.description,
            'status':                 status,
            'note':                   board_goal.note,
            'user_id':                board_goal.user_id,
            'user_label':             board_goal.user.name,
            'objectives':             objs,
        }


class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        board_goal = BoardGoal.objects.get(pk=data['id'])
        objectives = list(board_goal.boardgoalobjectives_set.values('id', 'result', 'description', 'note'))
        return {
            'id':                     board_goal.id,
            'board_id':               board_goal.board_id,
            'name':                   board_goal.name,
            'description':            board_goal.description,
            'status':                 board_goal.status,
            'note':                   board_goal.note,
            'user_id':                board_goal.user_id,
            'user_label':             board_goal.user.name,
            'objectives':             objectives,
        }

class GetBulkUpdate(handlers.standard.ListHandler):
    def create_query(self, data):
        query = BoardGoal.objects
        board_id = data['board_id']
        query = query.filter(board_id=board_id)
        return query
    def serialize_entry(self, board_goal):
        return {
            'id':                     board_goal.id,
            'board_id':               board_goal.board_id,
            'name':                   board_goal.name,
            'description':            board_goal.description,
            'status':                 board_goal.status,
            'note':                   board_goal.note,
            'user_id':                board_goal.user_id,
            'user_label':             board_goal.user.name
        }

class Create(handlers.standard.CreateHandler):
    def create(self, data):
        print data
        goal = BoardGoal()
        goal.board_id = data.get('board_id', 0)
        if data.get('name', ''):
            goal.name = data.get('name', '')
        if data.get('description', ''):
            goal.description = data.get('description', '')
        if data.get('note', ''):
            goal.note = data.get('note', '')
        if data.get('status', ''):
            goal.status = data.get('status', '')
        if data.get('user_id', 0):
            goal.user_id = data.get('user_id', 0)
        goal.save()
        
        if data.get('objectives', ''):
            objectives = []
            goal_id = goal.id
            for obj in data['objectives']:
                objective = BoardGoalObjectives(
                    board_goal_id=goal_id,
                    description=obj.get('description', ''),
                    result=obj.get('result', ''),
                    note=obj.get('note', ''),
                )
                objectives.append(objective)
            BoardGoalObjectives.objects.bulk_create(objectives)
        return goal


class Update(handlers.standard.UpdateHandler):
    def update(self, data):
        goal = BoardGoal.objects.get(pk=data['id'])
        if data.get('name', ''):
            goal.name = data.get('name', '')
        if data.get('description', ''):
            goal.description = data.get('description', '')
        if data.get('status', ''):
            goal.status = data.get('status', '')
        if data.get('user_id', 0):
            goal.user_id = data.get('user_id', 0)
        if data.get('note', ''):
            goal.note = data.get('note', '')
        if data.get('objectives', ''):
            goal_id = goal.id
            BoardGoalObjectives.objects.filter(board_goal_id=goal_id).delete()
            objectives = []
            for obj in data['objectives']:
                objective = BoardGoalObjectives(
                    board_goal_id=goal_id,
                    description=obj.get('description', ''),
                    result=obj.get('result', ''),
                    note=obj.get('note', ''),
                )
                objectives.append(objective)
            BoardGoalObjectives.objects.bulk_create(objectives)
        goal.save()
        return goal

class BulkUpdate(handlers.standard.UpdateHandler):
    def update(self, data):
        goal = {}
        for val in data['goal']:
            goal = BoardGoal.objects.get(pk=val.get('id'))
            goal.user_id = val.get('user_id', 0)
            if val.get('name', ''):
                goal.name = val.get('name', '')
            if val.get('status', ''):
                goal.status = val.get('status', '')
            goal.save()
        return goal

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        goal = BoardGoal.objects.get(pk=data['id'])
        goal.delete()
        return 1
