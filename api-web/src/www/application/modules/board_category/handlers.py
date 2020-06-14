from django.contrib.humanize.templatetags.humanize import naturaltime
from notasquare.urad_api import *
from application.models import *
from application import constants
from application.modules.common import helpers


class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = BoardCategory.objects
        board_id = data.get('board_id', 0)
        query = query.filter(board_id=board_id)
        if data.get('text', '') != '' :
            query = query.filter(name__contains=data['text'])
        return query
    def serialize_entry(self, board_category):
        num_story = BoardStory.objects.filter(board_id = board_category.board_id, board_category_id = board_category.id).count()
        return  {
            'id':             board_category.id,
            'board_id':       board_category.board_id,
            'name':           board_category.name,
            'description':    board_category.description,
            'manager_id':     board_category.manager_id,
            'manager_label':  board_category.manager.name,
            'num_story':      num_story
        }


class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        board_category = BoardCategory.objects.get(pk=data['id'])

        stages = []
        records = BoardCategoryStage.objects.filter(board_category=board_category.id)
        for r in records:
            stages.append({
                'id':                  r.id,
                'board_stage_id':      r.board_stage_id,
                'board_stage_label':   r.board_stage.name,
                'manager_id':          r.manager_id,
                'manager_label':       r.manager.name,
            })

        goals = []
        records = BoardGoal.objects.filter(board_category_id=board_category.id)
        for r in records:
            goals.append({
                'id':                  r.id,
                'name':                r.name,
                'status':              r.status
            })

        responsibilities = []
        records = BoardCategoryResponsibility.objects.filter(board_category_id=board_category.id).all()
        for r in records:
            responsibilities.append({
                'user_id':        r.user_id,
                'user_label':     r.user.name,
                'description':    r.description
            })


        return {
            'id':                board_category.id,
            'board_id':          board_category.board_id,
            'name':              board_category.name,
            'description':       board_category.description,
            'manager_id':        board_category.manager_id,
            'manager_label':     board_category.manager.name,
            'stages':            stages,
            'goals':             goals,
            'responsibilities':  responsibilities
        }


class Create(handlers.standard.CreateHandler):
    def create(self, data):
        category = BoardCategory()
        category.board_id = data.get('board_id', 0)
        if data.get('name', ''):
            category.name = data.get('name', '')
        if data.get('description', ''):
            category.description = data.get('description', '')
        if data.get('manager_id', 0):
            category.manager_id = data.get('manager_id', 0)
        category.save()

        if data.get('stages', ''):
            for r in data['stages']:
                category_stage = BoardCategoryStage()
                category_stage.board_category_id = category.id
                category_stage.board_stage_id = r['board_stage_id']
                category_stage.manager_id = r['manager_id']
                category_stage.save()

        if data.get('responsibilities', ''):
            for r in data.get('responsibilities'):
                responsibility = BoardCategoryResponsibility()
                responsibility.board_category_id = category.id
                responsibility.user_id = r['user_id']
                responsibility.description = r['description']
                responsibility.save()

        helpers.CommonHelper().update_cell_assignment(category.board_id)

        return category


class Update(handlers.standard.UpdateHandler):
    def update(self, data):
        category = BoardCategory.objects.get(pk=data['id'])
        if data.get('name', ''):
            category.name = data.get('name', '')
        if data.get('description', ''):
            category.description = data.get('description', '')
        if data.get('manager_id', 0):
            category.manager_id = data.get('manager_id', 0)
        category.save()

        if data.get('stages', ''):
            BoardCategoryStage.objects.filter(board_category_id=category.id).delete()
            for r in data['stages']:
                category_stage = BoardCategoryStage()
                category_stage.board_category_id = category.id
                category_stage.board_stage_id = r['board_stage_id']
                category_stage.manager_id = r['manager_id']
                category_stage.save()

        if data.get('responsibilities', ''):
            BoardCategoryResponsibility.objects.filter(board_category_id=category.id).delete()
            for r in data.get('responsibilities'):
                responsibility = BoardCategoryResponsibility()
                responsibility.board_category_id = category.id
                responsibility.user_id = r['user_id']
                responsibility.description = r['description']
                responsibility.save()

        helpers.CommonHelper().update_cell_assignment(category.board_id)

        return category

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        category = BoardCategory.objects.get(pk=data['id'])
        category.delete()
        return 1
