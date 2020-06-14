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
        return components.QueueFullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '    <a class="btn btn-xs btn-primary" href="/queue/update/%s">Edit</a>' % (row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/queue/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
        def nl2br(self, s):
            return '<br />\n'.join(s.split('\n'))
        def render_cell_name(self, table, row):
            return '<text class="board-status" style="color: %s; background-color: %s">%s</text><br/><i>%s</i>' % (row['text_color'], row['bg_color'], row['name'], self.nl2br(row['description']))
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Queue')
        table.set_subtitle('List of queue')
        table.create_button('create', '/queue/create', 'zmdi-plus')
        table.create_column('id', 'ID', '6%', sortable=True)
        table.create_column('name', 'Name', '80%', sortable=True)
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.QueueStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        return components.QueueFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Queue')
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Textarea('description'))
        form.add_field(widgets.field.Textbox('bg_color'))
        form.add_field(widgets.field.Textbox('text_color'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Queue information')
        form.renderer.add_field('name', 'Name')
        form.renderer.add_field('description', 'Description', rows=5)
        form.renderer.add_field('text_color', 'Text color')
        form.renderer.add_field('bg_color', 'Background color')

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
            'text_color': '#000000',
            'bg_color': '#FFFFFF'
        })
    def process_form_data(self, data):
        return components.QueueStore(self.get_container()).create(data)


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        self.params['submenu'] = 'update'
        return components.QueueFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Queue')
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Textarea('description'))
        form.add_field(widgets.field.Textbox('bg_color'))
        form.add_field(widgets.field.Textbox('text_color'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Queue information')
        form.renderer.add_field('name', 'Name')
        form.renderer.add_field('description', 'Description', rows=5)
        form.renderer.add_field('text_color', 'Text color')
        form.renderer.add_field('bg_color', 'Background color')

        form.renderer.set_field_renderer('date_picker', renderers.widgets.field.DatePickerRenderer())
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())

        return form
    def load_form(self, form):
        result = components.QueueStore(self.get_container()).get(self.params['queue_id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        data['id'] = self.params['queue_id']
        return components.QueueStore(self.get_container()).update(data)


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.QueueStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/queue/list')
