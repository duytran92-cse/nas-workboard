from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer
from . import components
from application.modules.user import components as user_components
from datetime import datetime

class List(actions.crud.ListAction):
    def create_page_context(self):
        return components.BoardFullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '    <a class="btn btn-xs btn-primary" href="/board/update/%s">Edit</a>' % (row['id'])
            if row.get('is_template', 0) != 0:
                html += '    <a class="btn btn-xs btn-info" href="/board/duplicate/%s">Duplicate</a>' % (row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/board/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
        def nl2br(self, s):
            return '<br />\n'.join(s.split('\n'))
        def render_cell_name(self, table, row):
            return "%s<br/><i>%s</i>" % (row['name'], self.nl2br(row['description']))
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Board')
        table.set_subtitle('List of boards')
        table.create_button('create', '/board/create', 'zmdi-plus')
        table.create_column('id', 'ID', '6%', sortable=True)
        table.create_column('name', 'Name', '50%', sortable=True)
        table.create_column('start_date', 'Start date', '10%')
        table.create_column('end_date', 'End date', '10%')
        table.create_column('status', 'Status', '10%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.BoardStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        return components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Board')
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Textarea('description'))
        form.add_field(widgets.field.DatePicker('start_date'))
        form.add_field(widgets.field.DatePicker('end_date'))
        form.add_field(widgets.field.Combobox('status', choices=constants.BOARD_STATUS))
        form.add_field(widgets.field.MultipleChoice('users', choices=user_components.UserStore(self.get_container()).populate_combobox()))
        form.add_field(widgets.field.Checkbox('is_template'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Board information')
        form.renderer.add_field('name', 'Name')
        form.renderer.add_field('description', 'Description', rows=5)
        form.renderer.add_field('start_date', 'Start date')
        form.renderer.add_field('end_date', 'End date')
        form.renderer.add_field('status', 'Status')
        form.renderer.add_field('users', 'Users')
        form.renderer.add_field('is_template', 'Is Template')

        ## Board Responsibility
        form.add_field(widgets.field.List('board_responsibility', {
            'id':            widgets.field.Textbox('id'),
            'manager':       widgets.field.Combobox('manager', choices=user_components.UserStore(self.get_container()).populate_combobox()),
            'description':   widgets.field.Textbox('description')
        }))
        form.renderer.add_section('Board - Responsibility')

        form.renderer.add_field('board_responsibility', '', columns=[
            {'id': 'manager',     'label': 'Manager',         'width': '10%'},
            {'id': 'description', 'label': 'Description',     'width': '70%'}
        ])

        form.renderer.set_field_renderer('date_picker', renderers.widgets.field.DatePickerRenderer())
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('checkbox', renderers.widgets.field.CheckboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
            'start_date': datetime.now().strftime("%Y-%m-%d")
        })
    def process_form_data(self, data):
        if data['start_date']:
            data['start_date'] = datetime.strptime(data['start_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
        if data['end_date']:
            data['end_date'] = datetime.strptime(data['end_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
        return components.BoardStore(self.get_container()).create(data)


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        self.params['submenu'] = 'update'
        return components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Board')
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Textarea('description'))
        form.add_field(widgets.field.DatePicker('start_date'))
        form.add_field(widgets.field.DatePicker('end_date'))
        form.add_field(widgets.field.Combobox('status', choices=constants.BOARD_STATUS))
        form.add_field(widgets.field.MultipleChoice('users', choices=user_components.UserStore(self.get_container()).populate_combobox()))
        form.add_field(widgets.field.Checkbox('is_template'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Board information')
        form.renderer.add_field('name', 'Name')
        form.renderer.add_field('description', 'Description', rows=5)
        form.renderer.add_field('start_date', 'Start date')
        form.renderer.add_field('end_date', 'End date')
        form.renderer.add_field('status', 'Status')
        form.renderer.add_field('users', 'Users')
        form.renderer.add_field('is_template', 'Is Template')

        ## Board Responsibility
        form.add_field(widgets.field.List('board_responsibility', {
            'id':            widgets.field.Textbox('id'),
            'manager':       widgets.field.Combobox('manager', choices=user_components.UserStore(self.get_container()).populate_combobox()),
            'description':   widgets.field.Textbox('description')
        }))
        form.renderer.add_section('Board - Responsibility')

        form.renderer.add_field('board_responsibility', '', columns=[
            {'id': 'manager',     'label': 'Manager',         'width': '10%'},
            {'id': 'description', 'label': 'Description',     'width': '70%'}
        ])

        form.renderer.set_field_renderer('date_picker', renderers.widgets.field.DatePickerRenderer())
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('checkbox', renderers.widgets.field.CheckboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        result = components.BoardStore(self.get_container()).get(self.params['board_id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        data['id'] = self.params['board_id']
        if data['start_date']:
            data['start_date'] = datetime.strptime(data['start_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
        if data['end_date']:
            data['end_date'] = datetime.strptime(data['end_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
        return components.BoardStore(self.get_container()).update(data)


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.BoardStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/board/list')


class Duplicate(actions.crud.CreateAction):
    def create_page_context(self):
        return components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Board')
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Textarea('description'))
        form.add_field(widgets.field.DatePicker('start_date'))
        form.add_field(widgets.field.DatePicker('end_date'))
        form.add_field(widgets.field.Combobox('status', choices=constants.BOARD_STATUS))
        form.add_field(widgets.field.MultipleChoice('users', choices=user_components.UserStore(self.get_container()).populate_combobox()))
        form.add_field(widgets.field.Checkbox('is_template'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Board information')
        form.renderer.add_field('name', 'Name')
        form.renderer.add_field('description', 'Description', rows=5)
        form.renderer.add_field('start_date', 'Start date')
        form.renderer.add_field('end_date', 'End date')
        form.renderer.add_field('status', 'Status')
        form.renderer.add_field('users', 'Users')
        form.renderer.add_field('is_template', 'Is Template')

        ## Board Responsibility
        form.add_field(widgets.field.List('board_responsibility', {
            'id':            widgets.field.Textbox('id'),
            'manager':       widgets.field.Combobox('manager', choices=user_components.UserStore(self.get_container()).populate_combobox()),
            'description':   widgets.field.Textbox('description')
        }))
        form.renderer.add_section('Board - Responsibility')

        form.renderer.add_field('board_responsibility', '', columns=[
            {'id': 'manager',     'label': 'Manager',         'width': '10%'},
            {'id': 'description', 'label': 'Description',     'width': '70%'}
        ])

        form.renderer.set_field_renderer('date_picker', renderers.widgets.field.DatePickerRenderer())
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('checkbox', renderers.widgets.field.CheckboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        result = components.BoardStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            if result['data']['record'].get('is_template', '') != '':
                result['data']['record']['is_template'] = False
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        
        if data['start_date']:
            data['start_date'] = datetime.strptime(data['start_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
        if data['end_date']:
            data['end_date'] = datetime.strptime(data['end_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
        if 'id' in self.params:
            data['id'] = self.params.get('id')
        res = components.BoardStore(self.get_container()).duplicate(data)
        return res