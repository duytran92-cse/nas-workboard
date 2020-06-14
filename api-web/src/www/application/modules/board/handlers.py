from django.contrib.humanize.templatetags.humanize import naturaltime
from notasquare.urad_api import *
from application.models import *
from application import constants
from django.db.models import Q, Count
from datetime import datetime
from application.modules.common import helpers
from collections import OrderedDict

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = Board.objects
        if data.get('text', '') != '' :
            query = query.filter(name__contains=data['text'])
        return query
    def serialize_entry(self, board):
        return {
            'id':               board.id,
            'name':             board.name,
            'description':      board.description,
            'start_date':       board.start_date,
            'end_date':         board.end_date,
            'status':           board.status,
            'is_template':      board.is_template,
        }

class GetHomeStatistics(handlers.standard.GetHandler):
    def get_story_stats(self, base_query):
        story_stats = []
        stats = base_query.order_by('board_stage__sort_order') \
            .values('board_stage_id') \
            .annotate(dcount=Count('board_stage_id')).all()
        for s in stats:
            board_stage = BoardStage.objects.get(pk=s['board_stage_id'])
            story_stats.append({
                'id':    board_stage.id,
                'name':  board_stage.name,
                'bg_color': board_stage.bg_color,
                'text_color': board_stage.text_color,
                'count': s['dcount']
            })
        return story_stats
    def get_goal_stats(self, base_query):
        goal_stats = []
        stats = base_query.values('status') \
            .annotate(dcount=Count('status')).all()
        for s in stats:
            goal_status = constants.BOARD_GOAL_STATUS_DATA[s['status']]
            goal_stats.append({
                'name':   goal_status['name'],
                'bg_color':   goal_status['bg_color'],
                'text_color':   goal_status['text_color'],
                'count':  s['dcount']
            })
        return goal_stats
    def get_data(self, data):
        record = {}
        try:
            board = Board.objects.get(pk=data['id'])
        except Board.DoesNotExist:
            return record
        else:
            # Story stats
            query = BoardStory.objects.filter(board_id = board.id)
            record['board_story_stats'] = self.get_story_stats(query)
            # Goal stats
            query = BoardGoal.objects.filter(board_id = board.id)
            record['board_goal_stats'] = self.get_goal_stats(query)
        return record

class GetStaticNumber(handlers.standard.GetHandler):

    def get_data(self, data):
        num_story = BoardStory.objects.filter(board_id = data['id']).count()
        num_goal  = BoardGoal.objects.filter(board_id = data['id']).count()
        num_event = BoardEvent.objects.filter(board_id = data['id']).count()
        num_your_story = BoardStory.objects.filter(Q(board_id = data['id']), Q(assignee = data['user_id']) | Q(manager_id = data['user_id'])).count()
        num_your_goal = BoardGoal.objects.filter(board_id = data['id'], user_id = data['user_id']).count()

        return {
            'num_story': num_story,
            'num_goal': num_goal,
            'num_event': num_event,
            'num_your_story': num_your_story,
            'num_your_goal': num_your_goal,
        }

class GetDashboard(handlers.standard.GetHandler):
    def get_story_stats(self, base_query):
        story_stats = []
        stats = base_query.order_by('board_stage__sort_order') \
            .values('board_stage_id') \
            .annotate(dcount=Count('board_stage_id')).all()
        for s in stats:
            board_stage = BoardStage.objects.get(pk=s['board_stage_id'])
            story_stats.append({
                'id':    board_stage.id,
                'name':  board_stage.name,
                'bg_color': board_stage.bg_color,
                'text_color': board_stage.text_color,
                'count': s['dcount']
            })
        return story_stats
    def get_goal_stats(self, base_query):
        goal_stats = []
        stats = base_query.values('status') \
            .annotate(dcount=Count('status')).all()
        for s in stats:
            goal_status = constants.BOARD_GOAL_STATUS_DATA[s['status']]

            goal_stats.append({
                'name':   goal_status['name'],
                'bg_color':   goal_status['bg_color'],
                'text_color':   goal_status['text_color'],
                'count':  s['dcount']
            })
        return goal_stats
    def get_request_stats(self, queue_id):
        request_stats = []
        stats = QueueRequest.objects.filter(queue_id=queue_id, board_id=None) \
            .values('status') \
            .annotate(dcount=Count('status')).all()
        for s in stats:
            request_status = constants.REQUEST_STATUS_DATA[s['status']]
            request_stats.append({
                'name':         request_status['name'],
                'bg_color':     request_status['bg_color'],
                'text_color':   request_status['text_color'],
                'count':        s['dcount']
            })
        return request_stats

    def get_data(self, data):
        ## YOUR QUEUES
        your_queues = []
        queues = Queue.objects.all()
        for queue in queues:
            your_queues.append({
                'id':               queue.id,
                'name':             queue.name,
                'description':      queue.description,
                'text_color':       queue.text_color,
                'bg_color':         queue.bg_color,
                'request_stats':    self.get_request_stats(queue.id)
            })

        ## YOUR BOARDS
        board_users = BoardUser.objects.filter(user_id=data['user_id'], board__status__in=constants.BOARD_ACTIVE_STATUS_LIST).order_by('board__end_date', 'board__name')
        your_boards = {}
        for board_user in board_users.all():
            board = board_user.board

            # Board data
            status_data = constants.BOARD_STATUS_DATA[board.status]
            record = {}
            record['board'] = {
                'id':               board.id,
                'name':             board.name,
                'description':      board.description,
                'start_date':       board.start_date.strftime('%d/%m/%Y'),
                'end_date':         board.end_date.strftime('%d/%m/%Y'),
                'status':           board.status,
                'status_label':     status_data['name'],
                'status_bg_color':  status_data['bg_color'],
                'status_text_color':  status_data['text_color'],
            }

            # Story stats
            query = BoardStory.objects.filter(Q(board_id = board.id), Q(assignee = data['user_id']) | Q(manager_id = data['user_id']))
            record['your_story_stats'] = self.get_story_stats(query)
            query = BoardStory.objects.filter(board_id = board.id)
            record['board_story_stats'] = self.get_story_stats(query)

            # Goal stats
            query = BoardGoal.objects.filter(Q(board_id = board.id), Q(user_id = data['user_id']))
            record['your_goal_stats'] = self.get_goal_stats(query)
            query = BoardGoal.objects.filter(board_id = board.id)
            record['board_goal_stats'] = self.get_goal_stats(query)

            # Board month
            cmonth = "%s/%s" % (board.end_date.month, board.end_date.year)
            if not cmonth in your_boards:
                your_boards[cmonth] = []
            your_boards[cmonth].append(record)

        return {
            'your_boards': your_boards,
            'your_queues': your_queues,
        }


class GetHome(handlers.standard.GetHandler):
    def get_data(self, data):
        current_user_id = data['user_id']
        arr_stories = []
        arr_your_board = []
        arr_your_goal  = []

        ## data board
        arr_board = []
        arr_event = []
        board = Board.objects.get(pk= data['id'])

        today = datetime.now()
        board_events=  BoardEvent.objects.filter(board_id=board.id, event_date__gte = today).order_by('event_date')
        for event in board_events:
            time_ago = helpers.CommonHelper().diff_time_today(event.event_date)
            arr_event.append({
                'id':                   event.id,
                'event_date':           event.event_date.strftime('%d-%m-%Y'),
                'event_day':            event.event_date.strftime("%d"),
                'event_month':          event.event_date.strftime('%m-%Y'),
                'name':                 event.name ,
                'board_id':             event.board_id,
                'timestamp':            time_ago
            })

        # Users
        board_users = []
        records = BoardUser.objects.filter(board_id=board.id)
        for r in records:
            board_users.append({
                'id':     r.user.id,
                'name':   r.user.name,
            })

        ## your goal
        board_goals = BoardGoal.objects.filter(user_id = current_user_id)
        for goal in board_goals:
            arr_your_goal.append({
                'id':           goal.id,
                'board_id':     goal.board_id,
                'name':         goal.name,
                'status':       goal.status,
                'category':     goal.board_category.name if goal.board_category else '',
                'username':     goal.user.name if goal.user else '',
                'user_id':      goal.user_id
            })


        return {
            'stories':                      arr_stories,
            'your_board':                   arr_your_board,
            'your_goal':                    arr_your_goal,
            'board_users':                  board_users,
            'event':                        arr_event
        }

class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        board = Board.objects.get(pk=data['id'])
        users = []
        board_responsibility = []
        records = BoardUser.objects.filter(board_id=board.id).all()
        board_responsibility_records = BoardResponsibility.objects.filter(board_id=board.id).all()
        for res in board_responsibility_records:
            board_responsibility.append({
                'id': res.id,
                'description': res.description,
                'manager': res.user_id
            })
        for r in records:
            users.append(r.user_id)

        return {
            'id':               board.id,
            'name':             board.name,
            'status':           board.status,
            'description':      board.description,
            'start_date':       board.start_date,
            'end_date':         board.end_date,
            'users':            users,
            'board_responsibility': board_responsibility,
            'is_template':      board.is_template,
        }

class GetAllUser(handlers.standard.GetHandler):
    def get_data(self, data):
        board = Board.objects.get(pk=data['id'])
        arr_user = []
        user_board = BoardUser.objects.filter(board_id = board.id)
        for val in user_board:
            query = User.objects.filter(id= val.user_id)
            if query:
                user = query[0]
                story = BoardStory.objects.filter(board_id = board.id, assignee = user.id)
                arr_user.append({
                    'id':           user.id,
                    'name':         user.name,
                    'num_story':    len(story),
                    'board_id':     board.id
                })

        return arr_user

class GetBoardTag(handlers.standard.GetHandler):
    def get_data(self, data):
        board = Board.objects.get(pk=data['id'])
        arr_tag = []
        tags = BoardTag.objects.filter(board_id = board.id, is_visible = True)
        for tag in tags:
            arr_tag.append({
                'id':           tag.id,
                'icon':         tag.icon,
                'name':         tag.name,
            })
        return arr_tag

class GetSummary(handlers.standard.GetHandler):
    def get_data(self, data):
        board = Board.objects.get(pk=data['id'])
        arr_categories = []
        ## get Category
        categories = BoardCategory.objects.filter(board_id = board.id)
        arr_stories = []
        for category in categories:
            stories = BoardStory.objects.filter(board_category_id = category.id)
            for story in stories:
                arr_stories.append({
                    'id':               story.id,
                    'board_id':         story.board_id,
                    'name':             story.name,
                    'assignee_id':      story.assignee_id,
                    'assignee_label':   story.assignee if story.assignee else '',
                    'stage_label':      story.board_stage.name,
                    'stage_id':         story.board_stage.id,
                    'category_id':      category.id,
                    'category_name':    category.name,
                })

        ## Get Goal
        goals = BoardGoal.objects.filter(board_id= board.id)
        arr_goals = []
        for goal in goals:
            category_name = ''
            if goal.board_category_id:
                category_name = goal.board_category.name
            arr_goals.append({
                'id':           goal.id,
                'name':         goal.name,
                'status':       goal.status,
                'category':     category_name,
                'username':     goal.user.name if goal.user else '',
                'user_id':      goal.user.id

            })
        return {
            'id':               board.id,
            'name':             board.name,
            'description':      board.description,
            'start_date':       board.start_date,
            'end_date':         board.end_date,
            'category_stories': arr_stories,
            'goals':            arr_goals
        }

class GetCellAssignment(handlers.standard.GetHandler):
    def get_data(self, data):
        assignments = {}
        records = BoardCellAssignment.objects.filter(board_id=data['id']).all()
        for r in records:
            assignments["%s-%s" % (r.board_stage_id, r.board_category_id)] = {
                'manager_id':       r.manager_id,
                'manager_label':    r.manager.name if r.manager != None else ''
            }
        return assignments

class GetBoardResponsibility(handlers.standard.GetHandler):
    def get_data(self, data):
        board_user = BoardUser.objects.filter(board_id = data['id'])
        responsibility = []
        for row in board_user:
            description = []
            records = BoardResponsibility.objects.filter(board_id = data['id'], user_id = row.user_id)
            if records:
                username = ''
                for record in records:
                    username = record.user.name
                    description.append({
                        'id': record.id,
                        'description': record.description
                    })

                responsibility.append({
                    'user_id':                  row.id,
                    'board_id':                 row.board_id,
                    'username':                 username,
                    'des_responsibility':       description
                })
        return responsibility

class Create(handlers.standard.CreateHandler):
    def create(self, data):
        board = Board()
        board.name = data.get('name', '')
        board.description = data.get('description', '')
        if data.get('status', ''):
            board.status = data.get('status')
        if data.get('start_date', ''):
            board.start_date = data.get('start_date')
        if data.get('end_date', ''):
            board.end_date = data.get('end_date')
        board.is_template = 1 if data.get('is_template', '') == 'on' else 0
        board.save()

        if data.get('users', ''):
            for user_id in data['users']:
                board_user = BoardUser()
                board_user.board_id = board.id
                board_user.user_id = user_id
                board_user.save()

        if data.get('board_responsibility', ''):
            for resp in data['board_responsibility']:
                board_responsibility = BoardResponsibility()
                board_responsibility.board_id = board.id
                board_responsibility.user_id = resp['manager']
                board_responsibility.description = resp['description']
                board_responsibility.save()

        return board


class Duplicate(handlers.standard.CreateHandler):
    def create(self, data):
        if data.get('id', 0) == 0:
            return 1

        root_board = Board.objects.get(pk=data.get('id'))
        board = Board()
        board.name = data.get('name', '')
        board.description = data.get('description', '')
        if data.get('status', ''):
            board.status = data.get('status')
        if data.get('start_date', ''):
            board.start_date = data.get('start_date')
        if data.get('end_date', ''):
            board.end_date = data.get('end_date')
        if data.get('is_template', ''):
            board.is_template = data.get('is_template')
        board.save()

        #Tag
        tags = BoardTag.objects.filter(board_id = root_board.id)
        for val in tags:
            new_tag = BoardTag()
            new_tag.board_id = board.id
            new_tag.name = val.name
            new_tag.icon = val.icon
            new_tag.is_visible = val.is_visible
            new_tag.save()

        # - Users
        if data.get('users', ''):
            for user_id in data['users']:
                board_user = BoardUser()
                board_user.board_id = board.id
                board_user.user_id = user_id
                board_user.save()

        # - Responsibility
        if data.get('board_responsibility', ''):
            for resp in data['board_responsibility']:
                board_responsibility = BoardResponsibility()
                board_responsibility.board_id = board.id
                board_responsibility.user_id = resp['manager']
                board_responsibility.description = resp['description']
                board_responsibility.save()

        # - Stages
        try:
            stages = {}
            for r in BoardStage.objects.filter(board_id=root_board.id):
                old_id = int(r.id)
                r.board_id = board.id
                r.pk = None
                r.save()
                new_id = int(r.id)
                stages[old_id] = new_id
        except BoardStage.DoesNotExist:
            pass

        # - Categories
        try:
            categories = {}
            for r in BoardCategory.objects.filter(board_id=root_board.id):
                old_id = int(r.id)
                r.board_id = board.id
                r.pk = None
                r.save()
                new_id = int(r.id)
                categories[old_id] = new_id
        except BoardCategory.DoesNotExist:
            pass

        # - Categories Stage
        try:
            stages_mgrs = root_board.boardstage_set.exclude(manager_id=None).values_list('manager_id').distinct()
            category_mgrs = root_board.boardcategory_set.exclude(manager_id=None).values_list('manager_id').distinct()
            managers = list(stages_mgrs) + list(category_mgrs)
            for r in BoardCategoryStage.objects.filter(manager_id__in=managers):
                r.board_category_id = categories[r.board_category_id]
                r.board_stage_id = stages[r.board_stage_id]
                r.pk = None
                r.save()
        except BoardCategoryStage.DoesNotExist:
            pass

        # - Assignment
        helpers.CommonHelper().update_cell_assignment(board.id)

        # - Goals
        try:
            for r in BoardGoal.objects.filter(board_id=root_board.id):
                r.board_id = board.id
                r.pk = None
                r.save()
        except BoardGoal.DoesNotExist:
            pass

        return board


class Update(handlers.standard.UpdateHandler):
    def update(self, data):
        board = Board.objects.get(pk=data['id'])
        if data.get('name', ''):
            board.name = data.get('name', '')
        if data.get('description', ''):
            board.description = data.get('description', '')
        if data.get('status', ''):
            board.status = data.get('status')
        if data.get('start_date', ''):
            board.start_date = data.get('start_date', '')
        if data.get('end_date', ''):
            board.end_date = data.get('end_date', '')
        board.is_template = 1 if data.get('is_template', '') == 'on' else 0
        board.save()
        if data.get('users', ''):
            BoardUser.objects.filter(board_id=board.id).delete()
            for user_id in data['users']:
                board_user = BoardUser()
                board_user.board_id = board.id
                board_user.user_id = user_id
                board_user.save()

        if data.get('board_responsibility', ''):
            ## Delete old data
            BoardResponsibility.objects.filter(board_id = board.id).delete()
            for resp in data['board_responsibility']:
                board_responsibility = BoardResponsibility()
                board_responsibility.board_id = board.id
                board_responsibility.user_id = resp['manager']
                board_responsibility.description = resp['description']
                board_responsibility.save()
        return board

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        board = Board.objects.get(pk=data['id'])
        board.delete()
        return 1


class GetReport(handlers.standard.GetHandler):
    def get_summary_team(self, board_id):
        data = []
        try:
            for u in BoardUser.objects.filter(board_id=board_id).order_by('user_id__name'):
                item = {}
                try:
                    record = []
                    for bres in BoardResponsibility.objects.filter(board_id=board_id, user_id=u.user.id):
                        record.append(bres.description)
                except BoardResponsibility.DoesNotExist:
                    pass
                item['name'] = u.user.name
                item['role'] = []

                data.append(item)
        except BoardUser.DoesNotExist:
            pass

        return data

    def get_summary_story(self, board_id):
        data = {'users': [], 'total': {}, 'tbl_header': {}}
        try:
            header = {}
            for stage in BoardStage.objects.filter(board_id=board_id).order_by('id'):
                header[int(stage.id)] = {
                    'text_color': stage.text_color,
                    'bg_color': stage.bg_color,
                    'name': stage.name,
                }
            data['tbl_header'] = header
        except Exception as e:
            raise e
        try:
            total = {}
            for u in BoardUser.objects.filter(board_id=board_id).order_by('user_id__name'):
                record = {}
                for c in BoardStory.objects.filter(board_id=board_id, manager_id=u.user.id).values('board_stage_id', 'board_stage_id__name' ).annotate(count=Count('board_stage_id')).order_by('board_stage_id'):
                    # stage = c.get('board_stage_id__name').lower()
                    stage = int(c.get('board_stage_id'))
                    count = int(c.get('count', 0))

                    record[stage] = count
                    if stage not in total:
                        total[stage] = 0
                    total[stage] += count

                # story = {}
                for stage_id in data['tbl_header'].keys():
                    if stage_id not in record:
                        record[stage_id] = 0
                    if stage_id not in total:
                        total[stage_id] = 0
                if int(sum(record.itervalues())) > 0:
                    item = {}
                    item['sum'] = sum(record.itervalues())
                    item['name'] = u.user.name
                    item['story'] = record
                    data['users'].append(item)

            data['total'] = total
        except BoardUser.DoesNotExist:
            pass

        return data

    def get_summary_goal(self, board_id):
        data = {'users': [], 'tbl_header':
            [
                constants.BOARD_GOAL_STATUS_DATA['active'],
                constants.BOARD_GOAL_STATUS_DATA['success'],
                constants.BOARD_GOAL_STATUS_DATA['failed'],
                constants.BOARD_GOAL_STATUS_DATA['rejected'],
            ]
        }
        try:
            for u in BoardUser.objects.filter(board_id=board_id).order_by('user_id__name'):
                record = {}
                for bg in BoardGoal.objects.filter(board_id=board_id, user_id=u.id).values('status' ).annotate(count=Count('status')):
                    record[bg.get('status')] = int(bg.get('count', 0))
                record['sum'] = sum(record.itervalues())
                record['name'] = u.user.name
                data['users'].append(record)
        except BoardUser.DoesNotExist:
            pass

        return data

    def get_detail_story(self, board_id):
        data = []
        try:
            for u in BoardUser.objects.filter(board_id=board_id).order_by('user_id__name'):
                record = []
                for bs in BoardStory.objects.filter(board_id=board_id, manager_id=u.user_id):
                    r = {}
                    r['status'] = {
                        'name': bs.board_stage.name,
                        'text_color': bs.board_stage.text_color,
                        'bg_color': bs.board_stage.bg_color,
                    }
                    r['name'] = bs.name
                    r['category'] = bs.board_category.name
                    r['rating'] = {}
                    try:
                        rating = BoardStoryRating.objects.get(story_id=bs.id)
                        r['rating'] = {'name': rating.user.name, 'rating': rating.rating, 'description': rating.description}
                    except BoardStoryRating.DoesNotExist:
                        pass
                    record.append(r)
                if len(record) >0:
                    item = {}
                    item['story'] = record
                    item['name'] = u.user.name
                    data.append(item)
        except BoardUser.DoesNotExist:
            raise e
        return data

    def get_detail_goal(self, board_id):
        data = []
        try:
            for u in BoardUser.objects.filter(board_id=board_id):
                record = []

                for bg in BoardGoal.objects.filter(board_id=board_id, user_id=u.user_id):
                    r = {}
                    r['status'] = constants.BOARD_GOAL_STATUS_DATA[bg.status]
                    r['name'] = bg.name
                    r['objectives'] = {}
                    try:
                        for o in bg.boardgoalobjectives_set.values('result').annotate(count=Count('result')):
                            result = o.get('result', '').lower()
                            rc = {'count': o.get('count'), 'data': constants.OBJECTIVE_RESULTS_DATA[result]}
                            if result == 'active':
                                r['objectives'][result] = rc
                            if result == 'success':
                                r['objectives'][result] = rc
                            if result == 'failed':
                                r['objectives'][result] = rc
                            if result == 'rejected':
                                r['objectives'][result] = rc
                        record.append(r)
                    except BoardGoalObjectives:
                        pass
                if len(record) > 0:
                    item = {}
                    item['goal'] = record
                    item['name'] = u.user.name
                    data.append(item)

        except BoardUser.DoesNotExist:
            raise e
        return data

    def get_data(self, data):
        result = {}
        if data.get('id', 0) == 0:
            return result
        try:
            board = Board.objects.get(pk=data.get('id'))
            result = {
                'board_id': board.id,
                'board_name': board.name,
                'board_description': board.description,
                'summary': {
                    'team': self.get_summary_team(board.id),
                    'story': self.get_summary_story(board.id),
                    'goal': self.get_summary_goal(board.id),
                },
                'detail': {
                    'story': self.get_detail_story(board.id),
                    'goal': self.get_detail_goal(board.id),
                }
            }
        except Board.DoesNotExist:
            pass
        return result

class GetPerformanceReportData(handlers.standard.GetHandler):
    def get_data(self, data):
        result = []

        user_monthly_performances = UserMonthlyPerformance.objects.filter(year=data['year'], month=data['month']).order_by('user__name').all()
        for ump in user_monthly_performances:
            user_goals = []
            goals = BoardGoal.objects.filter(board__end_date__year=data['year'], board__end_date__month=data['month'], user_id=ump.user_id).all()
            for g in goals:
                user_goals.append({
                    'id':    g.id,
                    'board': g.board.name,
                    'goal':  g.name,
                    'result': g.status,
                })

            user_stories = []
            stories = BoardStory.objects.filter(board__end_date__year=data['year'], board__end_date__month=data['month'], manager_id=ump.user_id).all()
            for s in stories:
                user_stories.append({
                    'id':     s.id,
                    'story':  s.name,
                    'result': s.board_stage.result_code,
                    'rating': s.rating,
                    'notes':  s.notes,
                })

            result.append({
                'name': ump.user.name,
                'performance': {
                    'L':      ump.L,
                    'B':      ump.B,
                    'R':      ump.R,
                    'S':      ump.S,
                    'notes':  ump.notes,
                },
                'goals': user_goals,
                'stories': user_stories,
                'work_summaries': ump.summary.split("\n")
            })
        return result

class GetBoardReportData(handlers.standard.GetHandler):
    def get_board_team(self, board):
        team = []
        for r in BoardUser.objects.filter(board_id=board.id).all():
            team.append({
                'user': r.user.name,
                'workload': ''
            })
        return team
    def get_story_stats(self, board):
        stat = {
            'default':    0,
            'icebox':     0,
            'accepted':   0,
            'failed':     0,
        }
        for s in BoardStory.objects.filter(board_id=board.id).all():
            if s.board_stage.result_code in stat:
                stat[s.board_stage.result_code] += 1
            else:
                stat['default'] += 1
        return stat
    def get_goal_stats(self, board):
        stat = {
            'success':    0,
            'failed':     0,
            'rejected':   0
        }
        for g in BoardGoal.objects.filter(board_id=board.id).all():
            if g.status in stat:
                stat[g.status] += 1
            else:
                stat['rejected'] += 1
        return stat
    def get_goals(self, board):
        goals = []
        for g in BoardGoal.objects.filter(board_id=board.id).all():
            goals.append({
                'id':     g.id,
                'title':  g.name,
                'user':   g.user.name if g.user else '',
                'status': g.status,
            })
        return goals
    def get_stories(self, board):
        categories = {}
        for s in BoardStory.objects.filter(board_id=board.id).all():
            if not s.board_category_id in categories:
                categories[s.board_category_id] = {
                    'category': s.board_category.name,
                    'stories': []
                }
            categories[s.board_category_id]['stories'].append({
                'id':       s.id,
                'title':    s.name,
                'user':     s.manager.name if s.manager else '',
                'status':   s.board_stage.result_code,
            })

        stories = []
        for k, v in categories.iteritems():
            stories.append(v)
        return stories
    def get_data(self, data):
        result = {}

        board = Board.objects.get(pk=data['board_id'])
        result['board'] = {
            'id':          board.id,
            'name':        board.name,
            'team':        self.get_board_team(board),
            'story_stats': self.get_story_stats(board),
            'goal_stats':  self.get_goal_stats(board),
        }

        result['goals'] = self.get_goals(board)
        result['stories'] = self.get_stories(board)

        return result
