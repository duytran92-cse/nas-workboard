from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from . import constants


class User(models.Model):
    username = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')

class Board(models.Model):
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=255, default='', choices=constants.BOARD_STATUS)
    is_template = models.BooleanField(default=False)
    #new field
    new_description = models.TextField(default='')

class BoardResponsibility(models.Model):
    board = models.ForeignKey('Board')
    user = models.ForeignKey('User')
    description = models.TextField(default='')

class BoardGoal(models.Model):
    board = models.ForeignKey('Board')
    board_category = models.ForeignKey('BoardCategory', blank=True, null=True)
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    status = models.CharField(max_length=255, default='', choices=constants.BOARD_GOAL_STATUS)
    user = models.ForeignKey('User')
    note = models.TextField(default='')

class BoardGoalObjectives(models.Model):
    board_goal = models.ForeignKey('BoardGoal')
    description = models.TextField(default='')
    result = models.CharField(max_length=255, default='', choices=constants.OBJECTIVE_RESULTS)
    note = models.TextField(default='')

class BoardUser(models.Model):
    board = models.ForeignKey('Board')
    user = models.ForeignKey('User')

class BoardStage(models.Model):
    board = models.ForeignKey('Board')
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    manager = models.ForeignKey('User', blank=True, null=True)
    text_color = models.CharField(max_length=255, default='#000000')
    bg_color = models.CharField(max_length=255, default='transparent')
    sort_order = models.IntegerField(default=0)
    result_code = models.CharField(max_length=255, default='default')

class BoardNextStage(models.Model):
    board_stage_next = models.ForeignKey('BoardStage')
    board_stage_id   = models.IntegerField(default=0)

class BoardStageResponsibility(models.Model):
    board_stage = models.ForeignKey('BoardStage')
    user = models.ForeignKey('User')
    description = models.TextField(default='')

class BoardStageInstruction(models.Model):
    board_stage = models.ForeignKey('BoardStage')
    instruction = models.TextField(default='')

class BoardCategory(models.Model):
    board = models.ForeignKey('Board')
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    manager = models.ForeignKey('User')

class BoardCategoryResponsibility(models.Model):
    board_category = models.ForeignKey('BoardCategory')
    user = models.ForeignKey('User')
    description = models.TextField(default='')

class BoardCategoryStage(models.Model):
    board_category = models.ForeignKey('BoardCategory')
    board_stage = models.ForeignKey('BoardStage')
    manager = models.ForeignKey('User')

class BoardStory(models.Model):
    board = models.ForeignKey('Board')
    board_stage = models.ForeignKey('BoardStage')
    board_category = models.ForeignKey('BoardCategory')
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    assignee = models.ForeignKey('User', blank=True, null=True, related_name='assignee')
    manager = models.ForeignKey('User', blank=True, null=True, related_name='manager')
    is_active = models.BooleanField(default=True)
    last_update = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(default='.', max_length=1)
    notes = models.TextField(default='')

class BoardStoryRating(models.Model):
    story = models.ForeignKey('BoardStory')
    user = models.ForeignKey('User')
    description = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

class BoardStoryComment(models.Model):
    story = models.ForeignKey('BoardStory')
    user = models.ForeignKey('User')
    description = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)

class BoardStoryLog(models.Model):
    story = models.ForeignKey('BoardStory')
    user = models.ForeignKey('User')
    description = models.TextField(default='')
    assignee = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)

class BoardStoryTag(models.Model):
    story = models.ForeignKey('BoardStory')
    user = models.ForeignKey('User')
    tag = models.ForeignKey('BoardTag')
    value = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)

class BoardEvent(models.Model):
    board = models.ForeignKey('Board')
    event_date = models.DateField()
    name = models.CharField(max_length=255, default='')

class BoardTag(models.Model):
    board = models.ForeignKey('Board')
    name = models.TextField(default='')
    icon = models.CharField(max_length=255, default='')
    is_visible = models.BooleanField(default=True)

class BoardCellAssignment(models.Model):
    board = models.ForeignKey('Board')
    board_stage = models.ForeignKey('BoardStage')
    board_category = models.ForeignKey('BoardCategory')
    manager = models.ForeignKey('User', blank=True, null=True)

class BoardAssignment(models.Model):
    board = models.ForeignKey('Board')
    manager = models.ForeignKey('User')
    description = models.TextField(default='')


class Queue(models.Model):
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    text_color = models.CharField(max_length=255, default='#000000')
    bg_color = models.CharField(max_length=255, default='#FFFFFF')

class QueueRequest(models.Model):
    queue = models.ForeignKey('Queue')
    board = models.ForeignKey('Board', blank=True, null=True)
    title = models.TextField(default='')
    description = models.TextField(default='')
    requestor = models.ForeignKey('User', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0, choices=constants.REQUEST_PRIORITY)
    deadline = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=255, default='', choices=constants.REQUEST_STATUS)

class UserMonthlyPerformance(models.Model):
    user = models.ForeignKey('User')
    month = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    L = models.CharField(default='M', max_length=1)
    B = models.CharField(default='.', max_length=1)
    R = models.CharField(default='.', max_length=1)
    S = models.CharField(default='.', max_length=1)
    notes = models.TextField(default='')
    summary = models.TextField(default='')
