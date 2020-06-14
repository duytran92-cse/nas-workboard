
from application.models import *
from datetime import datetime

class CommonHelper(object):
    def update_cell_assignment(self, board_id):
        assignments = {}

        stages = BoardStage.objects.filter(board_id=board_id).all()
        categories = BoardCategory.objects.filter(board_id=board_id).all()

        if len(stages) == 0 or len(categories) == 0:
            return False

        for s in stages:
            for c in categories:
                assignments["%s-%s" % (s.id, c.id)] = None
        for c in categories:
            category_stages = BoardCategoryStage.objects.filter(board_category_id=c.id).all()
            for cs in category_stages:
                assignments["%s-%s" % (cs.board_stage_id, cs.board_category_id)] = cs.manager_id

        records = []
        BoardCellAssignment.objects.filter(board_id=board_id).delete()
        for k, manager_id in assignments.items():
            (stage_id, category_id) = k.split('-')
            cell_assignment = BoardCellAssignment()
            cell_assignment.board_id = board_id
            cell_assignment.board_stage_id = stage_id
            cell_assignment.board_category_id = category_id
            cell_assignment.manager_id = manager_id
            records.append(cell_assignment)
        BoardCellAssignment.objects.bulk_create(records)

    def diff_time(self, time_input):
        today = datetime.now()
        time_temp = time_input.strftime('%m/%d/%Y %H:%M:%S')
        time_temp = datetime.strptime(time_temp, "%m/%d/%Y %H:%M:%S")
        num = today - time_temp
        print num
        if (num.days > 0):
            month = num.days / 30
            if month > 0:
                year = month / 12
                if year > 0:
                    return str(year)+ "y"
                else:
                    return str(month)+ "M"
            else:
                return str(num.days)+ "d"
        elif (num.seconds > 0):
            minute = num.seconds / 60
            if minute > 0:
                hour = minute/60
                if (hour > 0):
                    return str(hour)+ "h"
                else:
                    return str(minute)+ "m"
            else:
                return str(num.seconds)+ "s"
        elif num.seconds == 0:
            return "Just now"

    def diff_time_today(self, time_input):
        today = datetime.now()
        time_temp = time_input.strftime('%m/%d/%Y %H:%M:%S')
        time_temp = datetime.strptime(time_temp, "%m/%d/%Y %H:%M:%S")
        num = time_temp - today
        if (num.days > 0):
            month = num.days / 30
            if month > 0:
                year = month / 12
                if year > 0:
                    return 'Next '+ str(year)+ " years"
                else:
                    return 'Next '+ str(month)+ " months"
            else:
                return 'Next '+ str(num.days)+ " days"
        elif num.days == 0:
            return "Today"
