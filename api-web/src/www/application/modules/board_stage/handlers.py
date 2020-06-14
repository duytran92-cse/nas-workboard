from django.contrib.humanize.templatetags.humanize import naturaltime
from notasquare.urad_api import *
from application.models import *
from application import constants
from application.modules.common import helpers



class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = BoardStage.objects
        board_id = data.get('board_id', 0)
        query = query.filter(board_id=board_id)
        if data.get('text', '') != '' :
            query = query.filter(name__contains=data['text'])
        return query
    def serialize_entry(self, board_stage):
        num_story = BoardStory.objects.filter(board_id = board_stage.board_id, board_stage_id = board_stage.id).count()
        return  {
            'id':             board_stage.id,
            'board_id':       board_stage.board_id,
            'name':           board_stage.name,
            'description':    board_stage.description,
            'manager_id':     board_stage.manager_id,
            'manager_label':  board_stage.manager.name if board_stage.manager != None else '',
            'bg_color':       board_stage.bg_color,
            'text_color':     board_stage.text_color,
            'sort_order':     board_stage.sort_order,
            'num_story':      num_story,
            'result_code':    board_stage.result_code,
        }


class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        board_stage = BoardStage.objects.get(pk=data['id'])

        instructions = []
        records = BoardStageInstruction.objects.filter(board_stage_id=board_stage.id).all()
        for r in records:
            instructions.append({
                'instruction': r.instruction
            })

        responsibilities = []
        records = BoardStageResponsibility.objects.filter(board_stage_id=board_stage.id).all()
        for r in records:
            responsibilities.append({
                'user_id':        r.user_id,
                'user_label':     r.user.name,
                'description':    r.description
            })

        return {
            'id':                board_stage.id,
            'board_id':          board_stage.board_id,
            'name':              board_stage.name,
            'description':       board_stage.description,
            'manager_id':        board_stage.manager_id,
            'manager_label':     board_stage.manager.name if board_stage.manager != None else '',
            'sort_order':        board_stage.sort_order,
            'instructions':      instructions,
            'responsibilities':  responsibilities,
            'bg_color':          board_stage.bg_color,
            'text_color':        board_stage.text_color,
            'result_code':       board_stage.result_code,
        }

class GetNextStage(handlers.standard.GetHandler):
    def get_data(self, data):
        board_next_stage = BoardNextStage.objects.filter(board_stage_id=data['id']).all()
        return {
            'id': board_next_stage.id,
            'board_next_stage_id': board_next_stage.board_next_stage_id,
            'board_next_stage_name': board_next_stage.board_next_stage.name,
            'board_stage_id': board_next_stage.board_stage_id
        }


class Create(handlers.standard.CreateHandler):
    def create(self, data):
        stage = BoardStage()
        stage.board_id = data.get('board_id', 0)
        if data.get('name', ''):
            stage.name = data.get('name', '')
        if data.get('description', ''):
            stage.description = data.get('description', '')
        if data.get('sort_order', 0):
            stage.sort_order = data.get('sort_order')
        if data.get('bg_color', '#FFFFFF'):
            stage.bg_color = data.get('bg_color', '#FFFFFF')
        if data.get('text_color', '#FFFFFF'):
            stage.text_color = data.get('text_color', '#000000')
        if data.get('result_code', ''):
            stage.result_code = data.get('result_code', '')
        stage.manager_id = data.get('manager_id', 0)
        stage.save()

        if data.get('instructions', ''):
            for r in data.get('instructions'):
                instruction = BoardStageInstruction()
                instruction.board_stage_id = stage.id
                instruction.instruction = r['instruction']
                instruction.save()

        if data.get('responsibilities', ''):
            for r in data.get('responsibilities'):
                responsibility = BoardStageResponsibility()
                responsibility.board_stage_id = stage.id
                responsibility.user_id = r['user_id']
                responsibility.description = r['description']
                responsibility.save()

        helpers.CommonHelper().update_cell_assignment(stage.board_id)

        return stage


class Update(handlers.standard.UpdateHandler):
    def update(self, data):
        stage = BoardStage.objects.get(pk=data['id'])
        if data.get('name', ''):
            stage.name = data.get('name', '')
        if data.get('description', ''):
            stage.description = data.get('description', '')
        if data.get('sort_order', 0):
            stage.sort_order = data.get('sort_order')

        if data.get('bg_color', '#000000'):
            stage.bg_color = data.get('bg_color', '#000000')
        if data.get('text_color', '#000000'):
            stage.text_color = data.get('text_color', '#000000')
        if data.get('result_code', ''):
            stage.result_code = data.get('result_code', '')

        stage.manager_id = data.get('manager_id', 0)
        stage.save()

        if data.get('instructions', ''):
            BoardStageInstruction.objects.filter(board_stage_id=stage.id).delete()
            for r in data.get('instructions'):
                instruction = BoardStageInstruction()
                instruction.board_stage_id = stage.id
                instruction.instruction = r['instruction']
                instruction.save()

        if data.get('responsibilities', ''):
            BoardStageResponsibility.objects.filter(board_stage_id=stage.id).delete()
            for r in data.get('responsibilities'):
                responsibility = BoardStageResponsibility()
                responsibility.board_stage_id = stage.id
                responsibility.user_id = r['user_id']
                responsibility.description = r['description']
                responsibility.save()

        helpers.CommonHelper().update_cell_assignment(stage.board_id)

        return stage

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        stage = BoardStage.objects.get(pk=data['id'])
        stage.delete()
        return 1
