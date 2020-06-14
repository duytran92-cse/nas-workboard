from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer
from . import components


class List(actions.crud.ListAction):
    def create_page_context(self):
        return components.UserFullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '    <a class="btn btn-xs btn-primary" href="/user/update/%s">Edit</a>' % (row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/user/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('User')
        table.set_subtitle('List of users')
        table.create_button('create', '/user/create', 'zmdi-plus')
        table.create_column('id', 'ID', '6%', sortable=True)
        table.create_column('username', 'Username', '20%', sortable=True)
        table.create_column('name', 'Name', '60%', sortable=True)
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.UserStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        return components.UserFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('User')
        form.add_field(widgets.field.Textbox('username'))
        form.add_field(widgets.field.Textbox('name'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('User information')
        form.renderer.add_field('username', 'Username')
        form.renderer.add_field('name', 'Name')
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
        })
    def process_form_data(self, data):
        return components.UserStore(self.get_container()).create(data)


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return components.UserFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('User')
        form.add_field(widgets.field.Textbox('username'))
        form.add_field(widgets.field.Textbox('name'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('User information')
        form.renderer.add_field('username', 'Username')
        form.renderer.add_field('name', 'Name')
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        return form
    def load_form(self, form):
        result = components.UserStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        data['id'] = self.params['id']
        return components.UserStore(self.get_container()).update(data)


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.UserStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/user/list')
