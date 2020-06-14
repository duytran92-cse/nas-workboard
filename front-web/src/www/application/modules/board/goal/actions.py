from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer
from . import components
from application.modules.board import components as board_components
from application.modules.common import page_contexts, actions as common_actions, components as common_components
from application.modules.user import components as user_components
from application.common import registry

class List(actions.crud.ListAction):
    def create_page_context(self):
        self.params['submenu'] = 'goal'
        self.params['page_title'] = 'Goal'
        if 'is_your_goal' in self.params:
            self.params['submenu'] = 'your_goal'
        return board_components.BoardFullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '    <a class="btn btn-xs btn-primary" href="/board/detail/%s/goal/update/%s">Edit</a>' % (row['board_id'], row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/board/detail/%s/goal/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['board_id'], row['id'])
            html += '</div>'
            return html
        def render_cell_user(self, table, row):
            return row['user_label']
        def render_cell_objectives(self, table, row):
            html = ''
            for x in row['objectives']:
                if x.get('name').lower() == 'pending':
                    html += '<span class="board-status" style="color: %s; background-color: %s; white-space: nowrap"><b> %s </b> %s</span>' % (x.get('text_color'), x.get('bg_color'), x.get('count', 0), x.get('name'))
                if x.get('name').lower() == 'pass':
                    html += '<span class="board-status" style="color: %s; background-color: %s; white-space: nowrap"><b> %s </b> %s</span>' % (x.get('text_color'), x.get('bg_color'), x.get('count', 0), x.get('name'))
                if x.get('name').lower() == 'failed':
                    html += '<span class="board-status" style="color: %s; background-color: %s; white-space: nowrap"><b> %s </b> %s</span>' % (x.get('text_color'), x.get('bg_color'), x.get('count', 0), x.get('name'))

            return html
        def render_cell_status(self, table, row):
            html = ''
            html += '<span class="board-status" style="color: %s; background-color: %s; white-space: nowrap"><b> %s </b></span> ' % (row['status'].get('text_color'), row['status'].get('bg_color'), row['status'].get('name'))
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Goals')
        table.set_subtitle('List of goals')
        table.create_button('create', '/board/detail/%s/goal/create' % (self.params['board_id']), 'Add', 'btn btn-sm bgm-cyan')
        table.create_button('bulk-update', '/board/detail/%s/goal/bulk-update' % (self.params['board_id']), 'Bulk-update', 'btn btn-sm btn-primary')
        table.create_column('id', 'ID', '6%', sortable=True)
        table.create_column('name', 'Name', '30%')
        table.create_column('user', 'User', '20%')
        table.create_column('objectives', 'Objectives', '20%')
        table.create_column('status', 'Status', '10%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.template = 'workboard/board/goal/table.html'
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        table_form_data['board_id'] = self.params['board_id']
        if 'is_your_goal' in self.params:
            print "USER", str(registry.USER['user_id'])
            table_form_data['user_id'] = registry.USER['user_id']
        return components.BoardGoalStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number=0)


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        self.params['submenu'] = 'goal'
        self.params['page_title'] = 'Create goal'
        return board_components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Goal')
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Texteditor('description'))
        form.add_field(widgets.field.Combobox('status', choices=constants.BOARD_GOAL_STATUS))
        form.add_field(widgets.field.Combobox('user_id', choices=user_components.UserStore(self.get_container()).populate_combobox()))
        form.add_field(widgets.field.List('objectives', {
            'description':          widgets.field.Textarea('description'),
            'result':               widgets.field.Combobox('result', choices=constants.OBJECTIVE_RESULTS),
            'note':                 widgets.field.Textarea('note')
        }))
        form.renderer = components.BoardGoalFormRenderer()
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('texteditor', renderers.widgets.field.TexteditorRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
        })
    def process_form_data(self, data):
        data['board_id'] = self.params['board_id']
        return components.BoardGoalStore(self.get_container()).create(data)
    def handle_on_success(self, messages):
        return HttpResponseRedirect('/board/detail/%s/goal/list' % (self.params['board_id']))


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        self.params['submenu'] = 'goal'
        self.params['page_title'] = 'Update goal' 
        return board_components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Goal')
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Texteditor('description'))
        form.add_field(widgets.field.Combobox('status', choices=constants.BOARD_GOAL_STATUS))
        form.add_field(widgets.field.Combobox('user_id', choices=user_components.UserStore(self.get_container()).populate_combobox()))
        form.add_field(widgets.field.List('objectives', {
            'description':          widgets.field.Textarea('description'),
            'result':               widgets.field.Combobox('result', choices=constants.OBJECTIVE_RESULTS),
            'note':                 widgets.field.Textarea('note')
        }))
        form.renderer = components.BoardGoalFormRenderer()
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('texteditor', renderers.widgets.field.TexteditorRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        result = components.BoardGoalStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        data['id'] = self.params['id']
        return components.BoardGoalStore(self.get_container()).update(data)
    def handle_on_success(self, messages):
        return HttpResponseRedirect('/board/detail/%s/goal/list' % (self.params['board_id']))


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.BoardGoalStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/board/detail/%s/goal/list' % (self.params['board_id']))
class BulkUpdate(actions.crud.UpdateAction, common_actions.BaseAction):
    def create_page_context(self):
        self.params['submenu'] = 'goal'
        return board_components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.add_field(widgets.field.List('goal', {
            'id':                   widgets.field.Textbox('id'),
            'name':                 widgets.field.Textbox('name'),
            'user_id':              widgets.field.Combobox('user_id', choices=user_components.UserStore(self.get_container()).populate_combobox()),
            'status':               widgets.field.Combobox('status', choices=constants.BOARD_GOAL_STATUS),
        }))
        form.renderer.add_section('Goal - Bulk Update')
        form.renderer.add_field('goal', 'Goal', columns=[
            {'id': 'id',                    'label': 'Id',          'width': '5%'},
            {'id': 'name',                  'label': 'Name',        'width': '25%'},
            {'id': 'user_id',               'label': 'User',        'width': '20%'},
            {'id': 'status',                'label': 'Status',      'width': '25%'},
        ])

        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListNonButtonRenderer())
        return form
    def load_form(self, form):
        result = components.BoardGoalStore(self.get_container()).get_bulk_update(self.params['board_id'])
        record = {}
        if result['status'] == 'ok':
            record['goal'] = result['data']['records']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.BoardGoalStore(self.get_container()).bulk_update(data)
