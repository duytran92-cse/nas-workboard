from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer
from . import components
from application.modules.queue import components as queue_components
from application.modules.user import components as user_components

class List(actions.crud.ListAction):
    def create_page_context(self):
        self.params['submenu'] = 'request'
        return queue_components.QueueFullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '    <a class="btn btn-xs btn-primary" href="/queue/detail/%s/request/update/%s">Edit</a>' % (row['queue_id'], row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/queue/detail/%s/request/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['queue_id'], row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Request')
        table.set_subtitle('List of requests')
        table.create_button('create', '/queue/detail/%s/request/create' % (self.params['queue_id']), 'zmdi-plus')
        table.create_column('id', 'ID', '6%', sortable=True)
        table.create_column('title', 'Title', '40%')
        table.create_column('requestor_label', 'Requestor', '10%')
        table.create_column('timestamp', 'Timestamp', '10%')
        table.create_column('priority', 'Priority', '10%')
        table.create_column('deadline', 'Deadline', '10%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        table_form_data['queue_id'] = self.params['queue_id']
        return components.QueueRequestStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        self.params['submenu'] = 'request'
        return queue_components.QueueFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Request')
        form.add_field(widgets.field.Textbox('title'))
        form.add_field(widgets.field.Texteditor('description'))
        form.add_field(widgets.field.Combobox('requestor_id', choices=user_components.UserStore(self.container).populate_combobox()))
        form.add_field(widgets.field.Textbox('deadline'))
        form.add_field(widgets.field.Combobox('priority', choices=constants.REQUEST_PRIORITY))
        form.add_field(widgets.field.Combobox('status', choices=constants.REQUEST_STATUS))

        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Request information')
        form.renderer.add_field('title', 'Title')
        form.renderer.add_field('description', 'Description')
        form.renderer.add_field('requestor_id', 'Requestor')
        form.renderer.add_field('deadline', 'Deadline')
        form.renderer.add_field('priority', 'Priority')
        form.renderer.add_field('status', 'Status')

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('texteditor', renderers.widgets.field.TexteditorRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
        })
    def process_form_data(self, data):
        data['queue_id'] = self.params['queue_id']
        return components.QueueRequestStore(self.get_container()).create(data)


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        self.params['submenu'] = 'request'
        return queue_components.QueueFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Request')
        form.add_field(widgets.field.Textbox('title'))
        form.add_field(widgets.field.Texteditor('description'))
        form.add_field(widgets.field.Combobox('requestor_id', choices=user_components.UserStore(self.container).populate_combobox()))
        form.add_field(widgets.field.Textbox('deadline'))
        form.add_field(widgets.field.Combobox('priority', choices=constants.REQUEST_PRIORITY))
        form.add_field(widgets.field.Combobox('status', choices=constants.REQUEST_STATUS))

        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Request information')
        form.renderer.add_field('title', 'Title')
        form.renderer.add_field('description', 'Description')
        form.renderer.add_field('requestor_id', 'Requestor')
        form.renderer.add_field('deadline', 'Deadline')
        form.renderer.add_field('priority', 'Priority')
        form.renderer.add_field('status', 'Status')

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('texteditor', renderers.widgets.field.TexteditorRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        result = components.QueueRequestStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        data['id'] = self.params['id']
        return components.QueueRequestStore(self.get_container()).update(data)


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.QueueRequestStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/queue/detail/%s/request/list' % (self.params['queue_id']))
