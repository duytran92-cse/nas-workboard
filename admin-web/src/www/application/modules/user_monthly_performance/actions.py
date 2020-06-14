from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer
from . import components
from application.modules.user import components as user_components

class List(actions.crud.ListAction):
    def create_page_context(self):
        return components.UserMonthlyPerformanceFullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '    <a class="btn btn-xs btn-primary" href="/user_monthly_performance/update/%s">Edit</a>' % (row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/user_monthly_performance/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
        def render_cell_month(self, table, row):
            return '%s/%s' % (row['month'], row['year'])
        def render_cell_user_id(self, table, row):
            return row['user_label']
        def render_cell_notes(self, table, row):
            return "%s<br/><br/>%s" % (row['notes'], row['summary'].replace("\n", "<br/>"))
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('User monthly performance')
        table.set_subtitle('List of user monthly performances')
        table.create_button('create', '/user_monthly_performance/create', 'zmdi-plus')
        table.create_column('id', 'ID', '6%', sortable=True)
        table.create_column('user_id', 'User', '15%', sortable=True)
        table.create_column('month', 'Month', '10%')
        table.create_column('L', 'L', '5%')
        table.create_column('B', 'B', '5%')
        table.create_column('R', 'R', '5%')
        table.create_column('S', 'S', '5%')
        table.create_column('notes', 'Notes', '35%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.UserMonthlyPerformanceStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        return components.UserMonthlyPerformanceFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('User monthly performance')
        form.add_field(widgets.field.Combobox('user_id', choices=user_components.UserStore(self.container).populate_combobox()))
        form.add_field(widgets.field.Textbox('month'))
        form.add_field(widgets.field.Textbox('year'))
        form.add_field(widgets.field.Textbox('L'))
        form.add_field(widgets.field.Textbox('B'))
        form.add_field(widgets.field.Textbox('R'))
        form.add_field(widgets.field.Textbox('notes'))
        form.add_field(widgets.field.Textarea('summary'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('User monthly performance')
        form.renderer.add_field('user_id', 'User')
        form.renderer.add_field('year', 'Year')
        form.renderer.add_field('month', 'Month')
        form.renderer.add_field('L', 'Workload')
        form.renderer.add_field('B', 'Behavior')
        form.renderer.add_field('R', 'Work Result')
        form.renderer.add_field('notes', 'Notes')
        form.renderer.add_field('summary', 'Summary', rows=10)
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        return form
    def load_form(self, form):
        form.set_form_data({
        })
    def process_form_data(self, data):
        return components.UserMonthlyPerformanceStore(self.get_container()).create(data)


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return components.UserMonthlyPerformanceFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('User monthly performance')
        form.add_field(widgets.field.Combobox('user_id', choices=user_components.UserStore(self.container).populate_combobox()))
        form.add_field(widgets.field.Textbox('month'))
        form.add_field(widgets.field.Textbox('year'))
        form.add_field(widgets.field.Textbox('L'))
        form.add_field(widgets.field.Textbox('B'))
        form.add_field(widgets.field.Textbox('R'))
        form.add_field(widgets.field.Textbox('notes'))
        form.add_field(widgets.field.Textarea('summary'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('User monthly performance')
        form.renderer.add_field('user_id', 'User')
        form.renderer.add_field('year', 'Year')
        form.renderer.add_field('month', 'Month')
        form.renderer.add_field('L', 'Workload')
        form.renderer.add_field('B', 'Behavior')
        form.renderer.add_field('R', 'Work Result')
        form.renderer.add_field('notes', 'Notes')
        form.renderer.add_field('summary', 'Summary', rows=10)
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        return form
    def load_form(self, form):
        result = components.UserMonthlyPerformanceStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        data['id'] = self.params['id']
        return components.UserMonthlyPerformanceStore(self.get_container()).update(data)


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.UserMonthlyPerformanceStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/user_monthly_performance/list')
