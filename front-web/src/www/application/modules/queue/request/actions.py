from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer
from . import components
from application.modules.user import components as user_components
from application.modules.queue import components as queue_components
from application.modules.common import page_contexts, actions as common_actions
from notasquare.urad_web.widgets import BaseWidget
from application.common import registry

class List(actions.crud.ListAction):
    def create_page_context(self):
        self.params['submenu'] = 'request'
        self.params['page_title']= 'Request'
        return queue_components.QueueFullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="checkbox m-b-15" style="margin-top:0px; margin-bottom: 0px !important">'
            html += '    <input type="hidden" id="request-id-%s" value=%s>' % (row['id'], row['id'])
            html += '    <input type="hidden" id="queue-id-%s" value=%s>' % (row['id'], row['queue_id'])
            html += '   <label>'
            html += '      <input type="checkbox" name="checkbox-request" id="%s" class="input">' % (row['id'])
            html += '      <i class="input-helper"></i>'
            html += '   </label>'
            html += '</div>'


            return html
        def render_cell_manager(self, table, row):
            return row['manager_label']
        def render_row(self, table, row):
            row_html = '<tr style="cursor:pointer">'
            if 'id' in row:
                row_html = '<tr val="'+ str(row['id'])+'" style="cursor:pointer">'
            for column in table.columns:
                method = 'render_cell_' + str(column.name)
                if column.name == 'actions':
                    f = getattr(self, method)
                    row_html += '<td>' + f(table, row) + '</td>'
                else:
                    if hasattr(self, method):
                        f = getattr(self, method)
                        row_html += '<td class="cell">' + f(table, row) + '</td>'
                    else:
                        row_html += '<td class="cell">' + (str(row[column.name]) if column.name in row else '') + '</td>'
            row_html += '</tr>'
            return row_html

        def render(self, table):
            template = loader.get_template(self.template)
            context = {}
            context['title'] = table.title
            context['subtitle'] = table.subtitle
            context['columns'] = table.columns
            context['buttons'] = table.buttons
            queue_id = ''
            rows_html = ''
            for row in table.data:
                queue_id  = row['queue_id']
                rows_html += self.render_row(table, row)
            context['rows_html'] = rows_html
            context['queue_id'] = queue_id
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Request')
        table.set_subtitle('List of requests')
        table.create_button('create', '/queue/detail/%s/request/create' % (self.params['queue_id']), 'Add', 'btn btn-sm bgm-cyan waves-effect')
        table.create_button('bulk-delete', '#', 'Delete', 'btn btn-sm btn-danger waves-effect')
        table.create_column('id', 'ID', '5%', sortable=True)
        table.create_column('title', 'Title', '45%')
        table.create_column('requestor_label', 'Requestor', '10%')
        table.create_column('deadline', 'Deadline', '10%')
        table.create_column('priority_label', 'Priority', '10%')
        table.create_column('status_label', 'Status', '10%')
        table.create_column('actions', '', '5%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.template = 'workboard/queue/request/table.html'
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        table_form_data['queue_id'] = self.params['queue_id']
        return components.QueueRequestStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number=0)
    def view_list_page(self):
        page_context = self.create_page_context()
        table = self.create_table()
        self.populate_table(table)
        page_context.add_widget(table)
        return HttpResponse(page_context.render())

class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        self.params['submenu'] = 'request'
        self.params['page_title']= 'Update request'
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

        form.renderer = components.RequestFormRenderer()
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('texteditor', renderers.widgets.field.TexteditorRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
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
        data['user_id'] = registry.USER['user_id']
        return components.QueueRequestStore(self.get_container()).update(data)
    def GET(self):
        page_context = self.create_page_context()
        form = self.create_form()
        self.load_form(form)
        page_context.add_widget(form)
        return HttpResponse(page_context.render())
    def handle_on_success(self, messages):
        return HttpResponseRedirect('/queue/detail/%s/request/list' % (self.params['queue_id']))


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        self.params['submenu'] = 'request'
        self.params['page_title']= 'Create request'
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

        form.renderer = components.RequestFormRenderer()
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
        data['queue_id'] = self.params['queue_id']
        data['user_id'] = registry.USER['user_id']
        return components.QueueRequestStore(self.get_container()).create(data)
    def handle_on_success(self, messages):
        return HttpResponseRedirect('/queue/detail/%s/request/list' % (self.params['queue_id']))

class BulkDelete(common_actions.BaseAction):
    def POST(self):
        rs = components.QueueRequestStore(self.get_container()).bulk_delete(self.params)
        return JsonResponse(rs)
