from django.contrib.humanize.templatetags.humanize import naturaltime
from notasquare.urad_api import *
from application.models import *
from application import constants

class List(handlers.standard.ListHandler):
    def create_query(self, data):
        query = UserMonthlyPerformance.objects
        if data.get('text', '') != '' :
            query = query.filter(name__contains=data['text'])
        return query
    def serialize_entry(self, user_monthly_performance):
        return {
            'id':               user_monthly_performance.id,
            'user_id':          user_monthly_performance.user_id,
            'user_label':       user_monthly_performance.user.name,
            'month':            user_monthly_performance.month,
            'year':             user_monthly_performance.year,
            'L':                user_monthly_performance.L,
            'B':                user_monthly_performance.B,
            'R':                user_monthly_performance.R,
            'S':                user_monthly_performance.S,
            'notes':            user_monthly_performance.notes,
            'summary':          user_monthly_performance.summary,
        }



class Get(handlers.standard.GetHandler):
    def get_data(self, data):
        user_monthly_performance = UserMonthlyPerformance.objects.get(pk=data['id'])
        return {
            'id':               user_monthly_performance.id,
            'user_id':          user_monthly_performance.user_id,
            'user_label':       user_monthly_performance.user.name,
            'month':            user_monthly_performance.month,
            'year':             user_monthly_performance.year,
            'L':                user_monthly_performance.L,
            'B':                user_monthly_performance.B,
            'R':                user_monthly_performance.R,
            'S':                user_monthly_performance.S,
            'notes':            user_monthly_performance.notes,
            'summary':          user_monthly_performance.summary,
        }

class Create(handlers.standard.CreateHandler):
    def create(self, data):
        p = UserMonthlyPerformance()
        p.user_id = data.get('user_id')
        p.year = data.get('year', 0)
        p.month = data.get('month', 0)
        p.L = data.get('L', 'M')
        p.B = data.get('B', '.')
        p.R = data.get('R', '.')
        p.notes = data.get('notes', '')
        p.summary = data.get('summary', '')
        p.S = '.'
        for s in constants.SCORING_SCHEMA:
            if s['L'] == p.L and s['B'] == p.B and s['R'] == p.R:
                p.S = s['S']
        p.save()
        return p


class Update(handlers.standard.UpdateHandler):
    def update(self, data):
        p = UserMonthlyPerformance.objects.get(pk=data['id'])
        if data.get('year', ''):
            p.year = data.get('year')
        if data.get('month', ''):
            p.month = data.get('month')
        if data.get('L', ''):
            p.L = data.get('L')
        if data.get('B', ''):
            p.B = data.get('B')
        if data.get('R', ''):
            p.R = data.get('R')
        if data.get('summary', ''):
            p.summary = data.get('summary')
        p.S = '.'
        for s in constants.SCORING_SCHEMA:
            if s['L'] == p.L and s['B'] == p.B and s['R'] == p.R:
                p.S = s['S']
        if data.get('notes', ''):
            p.notes = data.get('notes')
        p.save()
        return p

class Delete(handlers.standard.DeleteHandler):
    def delete(self, data):
        p = UserMonthlyPerformance.objects.get(pk=data['id'])
        p.delete()
        return 1
