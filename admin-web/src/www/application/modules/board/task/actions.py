from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer
from . import components
from application.modules.board import components as board_components
from application.modules.board.category import components as board_category_components
from application.modules.board.stage import components as board_stage_components
from application.modules.user import components as user_components

class List(actions.crud.ListAction):
    def create_page_context(self):
        self.params['submenu'] = 'task'
        return board_components.BoardFullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '    <a class="btn btn-xs btn-primary" href="/board/detail/%s/task/update/%s">Edit</a>' % (row['board_id'], row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/board/detail/%s/task/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['board_id'], row['id'])
            html += '</div>'
            return html
        def render_cell_manager(self, table, row):
            return row['manager_label']
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Task')
        table.set_subtitle('List of tasks')
        table.create_button('create', '/board/detail/%s/task/create' % (self.params['board_id']), 'zmdi-plus')
        table.create_column('id', 'ID', '6%', sortable=True)
        table.create_column('name', 'Name', '35%')
        table.create_column('manager', 'Manager', '15%', sortable=True)
        table.create_column('board_category_label', 'Category', '15%')
        table.create_column('board_stage_label', 'Stage', '15%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        table_form_data['board_id'] = self.params['board_id']
        return components.BoardTaskStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        self.params['submenu'] = 'task'
        return board_components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Task')
        form.add_field(widgets.field.Combobox('board_category_id', choices=board_category_components.BoardCategoryStore(self.get_container()).populate_combobox(self.params['board_id'])))
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Textarea('description'))
        form.add_field(widgets.field.Combobox('manager_id', choices=user_components.UserStore(self.get_container()).populate_combobox()))
        form.add_field(widgets.field.Combobox('board_stage_id', choices=board_stage_components.BoardStageStore(self.get_container()).populate_combobox(self.params['board_id'])))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Task information')
        form.renderer.add_field('board_category_id', 'Category')
        form.renderer.add_field('name', 'Name')
        form.renderer.add_field('description', 'Description', rows=5)
        form.renderer.add_field('manager_id', 'Manager')
        form.renderer.add_field('board_stage_id', 'Stage')
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
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
        return components.BoardTaskStore(self.get_container()).create(data)


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        self.params['submenu'] = 'task'
        return board_components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Task')
        form.add_field(widgets.field.Combobox('board_category_id', choices=board_category_components.BoardCategoryStore(self.get_container()).populate_combobox(self.params['board_id'])))
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Textarea('description'))
        form.add_field(widgets.field.Combobox('manager_id', choices=user_components.UserStore(self.get_container()).populate_combobox()))
        form.add_field(widgets.field.Combobox('board_stage_id', choices=board_stage_components.BoardStageStore(self.get_container()).populate_combobox(self.params['board_id'])))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Task information')
        form.renderer.add_field('board_category_id', 'Category')
        form.renderer.add_field('name', 'Name')
        form.renderer.add_field('description', 'Description', rows=5)
        form.renderer.add_field('manager_id', 'Manager')
        form.renderer.add_field('board_stage_id', 'Stage')
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        result = components.BoardTaskStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        data['id'] = self.params['id']
        return components.BoardTaskStore(self.get_container()).update(data)


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.BoardTaskStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/board/detail/%s/task/list' % (self.params['board_id']))
