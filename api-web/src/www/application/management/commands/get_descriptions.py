#get description for each board stage
from application.models import *
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		_inputString_ = 'The stage can be [In progress], [Pending], [Backlog], [Acceptance], [Accepted], [Failed], [Testing], [Icebox], [Quality Control]. Each stage contains some details explained in instruction text'

		#Step 1: Get all string between '[...]''
		_startIndex = []
		_endIndex = []

		_array_ = []

		_status_ = {}

		for _s_ in range(0, len(_inputString_)):
			if _inputString_[_s_] == '[':
				_startIndex.append(_s_ + 1)
			if _inputString_[_s_] == ']':
				_endIndex.append(_s_)

		#Step 2: Mapping _startIndex with _endIndex to create the complete string for board
		for _index_ in range(0, len(_startIndex)):
			for _k_index_ in range(0, len(_endIndex)):
				if _index_ == _k_index_:
					_array_.append(_inputString_[int(_startIndex[_index_]):int(_endIndex[_index_])])

		#Find color

		for _stage_ in BoardStage.objects.all().values('name').distinct():
			_status_[_stage_['name']] = {'bg_color': [], 'text_color': []}

			for __stage__ in BoardStage.objects.filter(name=_stage_['name']).values('bg_color').distinct():
				_status_[_stage_['name']]['bg_color'].append(__stage__['bg_color'])

			for __stage__ in BoardStage.objects.filter(name=_stage_['name']).values('text_color').distinct():
				_status_[_stage_['name']]['text_color'].append(__stage__['text_color'])


		for _key_ in _array_:
			if _inputString_.find(_key_) == -1:
				print 'Failed'
			else:
				for _stt_ in _status_:
					if _key_ == _stt_:
						_new_key_ = _key_.replace(_key_, "<a class='board-status' style='background-color=" + str(_status_.get(_stt_).get('bg_color')[0]) + '; text-color = ' + str(_status_.get(_stt_).get('text_color')[0] + "'" +  ">") + ' ' + _stt_ + " </a>")
						_inputString_ = _inputString_.replace(_key_, _new_key_).replace('[','').replace(']','')
		print _inputString_