from django.contrib.humanize.templatetags.humanize import naturaltime
from notasquare.urad_api import *
from application.models import *
from application import constants
from django.db.models import Q
from application.modules.common import helpers
from datetime import datetime

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = BoardStory.objects
        board_id = data.get('board_id', 0)
        query = query.filter(board_id=board_id)
        query = query.filter(is_active = True)
        if data.get('stage_id', 0) != 0:
            query = query.filter(board_stage_id=data.get('stage_id'))
        if data.get('category_id', 0) != 0:
            query = query.filter(board_category_id=data.get('category_id'))
        if data.get('user_id', 0) != 0:
            query = query.filter(Q(assignee_id = data.get('user_id')) | Q(manager_id = data.get('user_id')))
        if data.get('assignee_id', 0) != 0:
            query = query.filter(Q(assignee_id = data.get('assignee_id')))
        if data.get('text', '') != '' :
            query = query.filter(name__contains=data['text'])
        return query
    def serialize_entry(self, story):
        board_next_stage = BoardNextStage.objects.filter(board_stage_id=story.board_stage_id).all()
        board_stage = BoardStage.objects.filter(board_id=story.board_id).all()
        all_stage = []
        for val in board_stage:
            all_stage.append({
                'id': val.id,
                'name': val.name
            })

        ## get Tag
        arr_tags =[]
        story_tag = BoardStoryTag.objects.filter(story_id = story.id)
        for val in story_tag:
            arr_tags.append({
                'id':       val.id,
                'icon':     val.tag.icon,
                'info':     {
                        'tag_id':   val.tag.id,
                        'icon':     val.tag.icon,
                        'name':     val.tag.name,
                        'value':    val.value
                }
            })
        return {
            'id':                    story.id,
            'board_id':              story.board_id,
            'board_stage_id':        story.board_stage_id,
            'board_stage_label':     story.board_stage.name,
            'bg_color':              story.board_stage.bg_color,
            'text_color':            story.board_stage.text_color,
            'board_category_id':     story.board_category_id,
            'board_category_label':  story.board_category.name,
            'name':                  story.name,
            'description':           story.description,
            'assignee_id':           story.assignee_id,
            'assignee_label':        story.assignee.name if story.assignee else '',
            'manager_id':            story.manager_id,
            'manager_label':         story.manager.name if story.manager else '',
            'last_update':           story.last_update,
            'all_stage':             all_stage,
            'tags':                  arr_tags
        }



class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        story = BoardStory.objects.get(pk=data['id'])
        return {
            'id':                    story.id,
            'board_id':              story.board_id,
            'board_stage_id':        story.board_stage_id,
            'board_stage_label':     story.board_stage.name,
            'bg_color':              story.board_stage.bg_color,
            'text_color':            story.board_stage.text_color,
            'board_category_id':     story.board_category_id,
            'board_category_label':  story.board_category.name,
            'name':                  story.name,
            'description':           story.description,
            'assignee_id':           story.assignee_id,
            'assignee_label':        story.assignee.name if story.assignee else '',
            'manager_id':            story.manager_id,
            'manager_label':         story.manager.name if story.manager else '',
            'last_update':           story.last_update,
        }
class GetLogs(handlers.standard.GetHandler):
    def get_data(self, data):
        story = BoardStory.objects.get(pk=data['id'])
        ##get Logs
        logs = BoardStoryLog.objects.filter(story_id = story.id).order_by('-timestamp')[:10]
        arr_logs = []
        for log in logs:
            time_ago = helpers.CommonHelper().diff_time(log.timestamp)
            arr_logs.append({
                'id':               log.id,
                'username':         log.user.name,
                'user_id':          log.user.id,
                'description':      log.description,
                'timestamp':        time_ago,
                'assignee':         log.assignee
            })

        ##get Logs unlimit
        logs = BoardStoryLog.objects.filter(story_id = story.id).order_by('-timestamp')
        arr_logs_unlimit = []
        for log in logs:
            time_ago = helpers.CommonHelper().diff_time(log.timestamp)
            arr_logs_unlimit.append({
                'id':               log.id,
                'username':         log.user.name,
                'user_id':          log.user.id,
                'description':      log.description,
                'timestamp':        time_ago,
                'assignee':         log.assignee
            })
        return {
            'story_id':                   story.id,
            'array_logs':                 arr_logs,
            'array_log_unlimit':          arr_logs_unlimit
        }

class GetComments(handlers.standard.GetHandler):
    def get_data(self, data):
        story = BoardStory.objects.get(pk=data['id'])
        ##get Logs
        cmts = BoardStoryComment.objects.filter(story_id = story.id)
        arr_cmts = []
        for cmt in cmts:
            time_ago = helpers.CommonHelper().diff_time(cmt.timestamp)
            arr_cmts.append({
                'id': cmt.id,
                'username': cmt.user.name,
                'description': cmt.description,
                'timestamp': time_ago
            })
        return {
            'story_id':                    story.id,
            'board_id':                   story.board_id,
            'arr_cmts':                   arr_cmts
        }

class GetTags(handlers.standard.GetHandler):
    def get_data(self, data):
        story = BoardStory.objects.get(pk=data['id'])
        ## get Tags
        arr_tag = []
        tags = BoardStoryTag.objects.filter(story_id = story.id)
        for val in tags:
            arr_tag.append({
                'id':           val.id,
                'value':        val.value,
                'tag_id':       val.tag_id,
                'tag_name':     val.tag.name,
                'username':     val.user.name
            })
        return arr_tag

class AddTag(handlers.standard.CreateHandler):
    def create(self, data):
        tag = BoardStoryTag()
        tag.value = data.get('value', '')
        tag.story_id = data.get('story_id', 0)
        tag.tag_id = data.get('tag_id', 0)
        tag.user_id = data.get('user_id', 0)
        tag.save()
        return tag

class DeleteTag(handlers.standard.DeleteHandler):
    def delete(self, data):
        tag = BoardStoryTag.objects.get(pk=data['id'])
        tag.delete()
        return 1

class GetRating(handlers.standard.GetHandler):
    def get_data(self, data):
        story = BoardStory.objects.get(pk=data['id'])
        CLASS = {
            '+': 'rating-up',
            '-': 'rating-down',
            '.': 'rating-none',
        }

        return {
            'story_id': story.id,
            'board_id': story.board_id,
            'rating':   story.rating,
            'rating_active': CLASS[story.rating] if story.rating in CLASS else '',
            'notes':    story.notes
        }

class AddComments(handlers.standard.CreateHandler):
    def create(self, data):
        cmt = BoardStoryComment()
        cmt.story_id = data.get('story_id', 0)
        cmt.user_id = data.get('user_id', 0)
        cmt.description = data.get('description', "")
        cmt.save()
        return cmt

class Create(handlers.standard.CreateHandler):
    def create(self, data):
        story = BoardStory()
        story.board_id = data.get('board_id', 0)
        story.board_stage_id = data.get('board_stage_id', 0)
        story.board_category_id = data.get('board_category_id', 0)
        story.name = data.get('name', '')
        story.description = data.get('description', '')
        if data.get('manager_id', 0) != 0:
            story.manager_id = data['manager_id']
        if data.get('assignee_id', 0) != 0:
            story.assignee_id = data.get('assignee_id', 0)
        story.save()

        stage = BoardStage.objects.get(pk = story.board_stage_id)
        log = BoardStoryLog()
        log.user_id = data.get('user_id', 0)
        log.story_id = story.id
        log.description = stage.name
        if story.assignee_id:
            log.assignee = story.assignee.name
        log.save()

        return story


class Update(handlers.standard.UpdateHandler):
    def update(self, data):
        story = BoardStory.objects.get(pk=data['id'])
        stage_old = 0
        assignee_id_old = 0
        if data.get('board_stage_id', 0):
            stage_old = story.board_stage_id
            story.board_stage_id = data.get('board_stage_id', 0)
        if data.get('board_category_id', 0):
            story.board_category_id = data.get('board_category_id', 0)
        if data.get('name', ''):
            story.name = data.get('name', '')
        if data.get('description', ''):
            story.description = data.get('description', '')
        if data.get('manager_id', 0) != 0:
            story.manager_id = data['manager_id']
        if data.get('assignee_id', 0) != 0:
            assignee_id_old = story.assignee_id
            story.assignee_id = data['assignee_id']
        story.last_update = datetime.now()
        story.save()

        ## Log stage
        if (int(story.board_stage_id) != int(stage_old)) or (story.assignee_id != assignee_id_old):
            stage = BoardStage.objects.get(pk = story.board_stage_id)

            cell_assignment = BoardCellAssignment.objects.filter(board_stage_id=story.board_stage_id, board_category_id=story.board_category_id).first()
            if cell_assignment:
                if cell_assignment.manager_id:
                    story.assignee_id = cell_assignment.manager_id
                story.save()

            log = BoardStoryLog()
            log.user_id = data.get('user_id', 0)
            log.story_id = story.id
            log.description = stage.name
            if story.assignee_id:
                log.assignee = story.assignee.name
            log.save()
        return story

class UpdateRating(handlers.standard.UpdateHandler):
    def update(self, data):
        story = BoardStory.objects.get(pk=data['story_id'])
        story.rating = data.get('rating', '.')
        story.notes = data.get('notes', '')
        story.save()
        return story

class ChangeStage(handlers.standard.UpdateHandler):
    def update(self, data):
        for arr_story in data['arr_story_id']:
            story = BoardStory.objects.get(pk=arr_story)
            current_stage_id = story.board_stage_id

            story.board_stage_id = data['next_stage_id']
            story.last_update = datetime.now()
            story.save()

            ## Log stage
            if int(current_stage_id) != int(data['next_stage_id']):
                stage = BoardStage.objects.get(pk = data['next_stage_id'])
                cell_assignment = BoardCellAssignment.objects.filter(board_stage_id=story.board_stage_id, board_category_id=story.board_category_id).first()
                if cell_assignment:
                    if cell_assignment.manager_id:
                        story.assignee_id = cell_assignment.manager_id
                    story.save()

                log = BoardStoryLog()
                log.user_id = data.get('user_id', 0)
                log.story_id = story.id
                log.description = stage.name
                if story.assignee_id:
                    log.assignee = story.assignee.name
                log.save()
        return story

class BulkDelete(handlers.standard.UpdateHandler):
    def update(self, data):
        for arr_story in data['arr_story_id']:
            story = BoardStory.objects.get(pk=arr_story)
            story.delete()
        return story

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        story = BoardStory.objects.get(pk=data['id'])
        story.delete()
        return 1
