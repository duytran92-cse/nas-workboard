from django.contrib.humanize.templatetags.humanize import naturaltime
from notasquare.urad_api import *
from application.models import *
from application import constants
from django.db.models import Q, Count
from datetime import datetime
from application.modules.common import helpers
from collections import OrderedDict

#Part 1: Get Board in progress -> bg_color, text_color
class GetBoardStatistics(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {
        	'open': {'data': [], 'total':0},
        	'in_progress': {'data': [], 'total':0},
        	'completed': {'data': [], 'total':0},
        	'closed': {'data': [], 'total':0},
        }

        _status_ = {
        	'status': [],
        }

        for board in Board.objects.order_by('name').filter(status='open'):
        	record = {'name': board.name, 'bg_color': constants.BOARD_STATUS_DATA[board.status]['bg_color'], 'text_color': constants.BOARD_STATUS_DATA[board.status]['text_color']}
        	result['open']['data'].append(record)

        for board in Board.objects.order_by('name').filter(status='in_progress'):
        	record = {'name': board.name, 'bg_color': constants.BOARD_STATUS_DATA[board.status]['bg_color'], 'text_color': constants.BOARD_STATUS_DATA[board.status]['text_color']}
        	result['in_progress']['data'].append(record)

        for board in Board.objects.order_by('name').filter(status='completed'):
        	record = {'name': board.name, 'bg_color': constants.BOARD_STATUS_DATA[board.status]['bg_color'], 'text_color': constants.BOARD_STATUS_DATA[board.status]['text_color']}
        	result['completed']['data'].append(record)

        for board in Board.objects.order_by('name').filter(status='closed'):
        	record = {'name': board.name, 'bg_color': constants.BOARD_STATUS_DATA[board.status]['bg_color'], 'text_color': constants.BOARD_STATUS_DATA[board.status]['text_color']}
        	result['closed']['data'].append(record)
	
        for status in Board.objects.values('status').order_by('status').distinct():
      		record = { 'status': status['status'], 'bg_color': constants.BOARD_STATUS_DATA[status['status']]['bg_color'], 'text_color': constants.BOARD_STATUS_DATA[status['status']]['text_color'], 'total': Board.objects.filter(status=status['status']).count()}
        	_status_['status'].append(record)  

        result['open']['total'] = len(result['open']['data'])
        result['in_progress']['total'] = len(result['in_progress']['data'])
        result['completed']['total'] = len(result['completed']['data'])
        result['closed']['total'] = len(result['closed']['data'])

        
        return {
            'result': result,
            'status': _status_,
        }

        # #new fix
        # '''json format: result = {
        #         'status': '',
        #         'text_color': '',
        #         'bg_color': '',
        #         'boards': []
        #     }'''

        # _result_ = {}


        # for __status__ in Board.objects.all().order_by('status'):
        #     _result_[__status__.status] = {'name': __status__.status, 'bg_color': constants.BOARD_STATUS_DATA[__status__.status]['bg_color'], 'text_color': constants.BOARD_STATUS_DATA[__status__.status]['text_color'], 'boards': []}
        #     for __board__ in Board.objects.filter(status=__status__.status):
        #         _result_[__status__.status]['boards'].append(__board__.name)

        # return {
        #     '_result_': _result_,
        # }

#Part 2: Get Story in progress
class GetStoryInProgress(handlers.standard.GetHandler):
    def get_data(self, data):
        
        num_story_in_progress = BoardStory.objects.filter(board_stage__name='In Progress').count()

        data = {}

        for board in Board.objects.all():
            if board.name not in data:
                data[board.name] = []

        for story in BoardStory.objects.filter(board_stage__name='In Progress'):
            if story.board.name in data:
                if story.board.name not in data[story.board.name]:
                    data[story.board.name].append(story.name)
        data = { k: v for k, v in data.items() if v} # dict comprehension
                    
        return {
            'num_stories': num_story_in_progress,
            'data':data,
        }

#Part 3: Get user statistics
class GetUserStatistics(handlers.standard.GetHandler):
    def get_data(self, data):
        data = []

        number_of_user = User.objects.all().count()

        for user in User.objects.order_by('name').all():
            record = {}
            if user.name not in record:
                record[user.name] = {'stories_in_progress': [], 'stories_failed': [],'stories_pending': [], 'stories_acceptance': [],'stories_accepted': [],'stories_testing': [],'stories_icebox': [],'stories_backlog': []}
                for story in BoardStory.objects.filter(board_stage__name='Backlog', manager_id__name=user.name):
                    if story.manager.name in record:
                        if story.name not in record[story.manager.name]['stories_backlog']:
                            record[story.manager.name]['stories_backlog'].append(story.name)

                for story in BoardStory.objects.filter(board_stage__name='Pending', manager_id__name=user.name):
                    if story.manager.name in record:
                        if story.name not in record[story.manager.name]['stories_pending']:
                            record[story.manager.name]['stories_pending'].append(story.name)

                for story in BoardStory.objects.filter(board_stage__name='In Progress', manager_id__name=user.name):
                    if story.manager.name in record:
                        if story.name not in record[story.manager.name]['stories_in_progress']:
                            record[story.manager.name]['stories_in_progress'].append(story.name)

                for story in BoardStory.objects.filter(board_stage__name='Acceptance', manager_id__name=user.name):
                    if story.manager.name in record:
                        if story.name not in record[story.manager.name]['stories_acceptance']:
                            record[story.manager.name]['stories_acceptance'].append(story.name)

                for story in BoardStory.objects.filter(board_stage__name='Accepted', manager_id__name=user.name):
                    if story.manager.name in record:
                        if story.name not in record[story.manager.name]['stories_accepted']:
                            record[story.manager.name]['stories_accepted'].append(story.name)
                    
                for story in BoardStory.objects.filter(board_stage__name='Testing', manager_id__name=user.name):
                    if story.manager.name in record:
                        if story.name not in record[story.manager.name]['stories_testing']:  
                            record[story.manager.name]['stories_testing'].append(story.name)

                for story in BoardStory.objects.filter(board_stage__name='Icebox', manager_id__name=user.name):
                    if story.manager.name in record:
                        if story.name not in record[story.manager.name]['stories_icebox']:  
                            record[story.manager.name]['stories_icebox'].append(story.name)

                for story in BoardStory.objects.filter(board_stage__name='Failed', manager_id__name=user.name):
                    if story.manager.name in record:
                        if story.name not in record[story.manager.name]['stories_failed']:
                            record[story.manager.name]['stories_failed'].append(story.name)

            data.append(record)
                       
        return {
            'data': data,
            'number_user': number_of_user,
        }


#Part 4: Demo API for instruction page => get color for each stage in instruction

class InstructionDemo(handlers.standard.GetHandler):
    def get_data(self, data):
        result = {}
        for stage in BoardStage.objects.all().order_by('name').values('name').distinct():
            result[stage['name']] = {'old_description': [], 'bg_color': [], 'text_color': [], 'new_description': []}

            for _stage_ in BoardStage.objects.filter(name=stage['name']).values('description').distinct():
                result[stage['name']]['old_description'].append(_stage_.get('description'))

            for _stage_ in BoardStage.objects.filter(name=stage['name']).values('bg_color').distinct():
                result[stage['name']]['bg_color'].append(_stage_.get('bg_color'))

            for _stage_ in BoardStage.objects.filter(name=stage['name']).values('text_color').distinct():
                result[stage['name']]['text_color'].append(_stage_.get('text_color'))


        #===> if yes, please change the JSONResponse to return new data


        #Step 1: Get all string between '[]' of old_description'
        # for key in result:
        #     print result.get(key).get('old_description')


        _startIndex = []
        _endIndex = []

        _array_ = []
        _inputDescription = ""

        #inputDescription is result.get(___stageName___).get('old_description')
        for k in result:
            #==> get key
            for s in range(0, len(result.get(k).get('old_description'))):
                # print len(str(result.get(k).get('old_description')[s]))
                for j in range(0, len(str(result.get(k).get('old_description')[s]))):
                    if str(result.get(k).get('old_description')[s])[j] == '[':
                        _startIndex.append(j + 1)
                    if str(result.get(k).get('old_description')[s])[j] == ']':
                        _endIndex.append(j)
                        for _index_ in range(0, len(_startIndex)):
                            for _k_index_ in range(0, len(_endIndex)):
                                print result.get(k).get('old_description')[s][j]
                                # _array_.append(str(result.get(k).get('old_description')[s][j][int(_startIndex[_index_])]:28))
                                print str(result.get(k).get('old_description')[s])

        print _array_
        # print _startIndex
        # print _endIndex












        # print result.get('In progress').get('old_description')[2]
        # for key in result:
        #     for description in result.get(key).get('old_description'):
        #         print description
        #         # for index in range(0, len(description)):
        #         #     if description[index] == '[':
        #         #         _startIndex.append(index + 1)
        #         #     if description[index] == ']':
        #         #         _endIndex.append(index)

        #         # print _startIndex
        #         # print _endIndex



        return result