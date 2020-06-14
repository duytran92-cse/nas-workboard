from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer
from . import components
from application.modules.board import components as board_components
from application.modules.user import components as user_components
from datetime import datetime

class List(actions.crud.ListAction):
    def create_page_context(self):
        self.params['submenu'] = 'event'
        self.params['page_title'] = 'Event'
        return board_components.BoardFullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '    <a class="btn btn-xs btn-primary" href="/board/detail/%s/event/update/%s">Edit</a>' % (row['board_id'], row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/board/detail/%s/event/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['board_id'], row['id'])
            html += '</div>'
            return html
        def render_cell_user(self, table, row):
            return row['user_label']
        def render_cell_event_date(self, table, row):
            today = datetime.now()
            inday = datetime.strptime(row['event_date'], "%Y-%m-%d")
            print today.strftime('%m-%d-%Y')
            if today > inday:
                num_of_day = today - inday
                return str(num_of_day.days) + " days ago"
            else:
                num_of_day = inday - today
                return "in "+ str(num_of_day.days) + " days"


    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Events')
        table.set_subtitle('List of events')
        table.create_button('create', '/board/detail/%s/event/create' % (self.params['board_id']), 'Add', 'btn btn-sm bgm-cyan')
        table.create_column('id', 'ID', '6%', sortable=True)
        table.create_column('event_date', 'Event date', '20%')
        table.create_column('name', 'Name', '60%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.template = 'workboard/board/event/table.html'
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        table_form_data['board_id'] = self.params['board_id']
        return components.BoardEventStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number=0)


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        self.params['submenu'] = 'event'
        self.params['page_title'] = 'Create event'
        return board_components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Event')
        form.add_field(widgets.field.DatePicker('event_date'))
        form.add_field(widgets.field.Textbox('name'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_field('event_date', 'Date')
        form.renderer.add_field('name', 'Name')
        form.renderer.set_field_renderer('date_picker', renderers.widgets.field.DatePickerRenderer())
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
        if data['event_date']:
            data['event_date'] = datetime.strptime(data['event_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
        else:
            data['event_date'] = datetime.now().strftime("%Y-%m-%d")
        return components.BoardEventStore(self.get_container()).create(data)


class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        self.params['submenu'] = 'event'
        self.params['page_title'] = 'Update event' 
        return board_components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Event')
        form.add_field(widgets.field.DatePicker('event_date'))
        form.add_field(widgets.field.Textbox('name'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_field('event_date', 'Date')
        form.renderer.add_field('name', 'Name')
        form.renderer.set_field_renderer('date_picker', renderers.widgets.field.DatePickerRenderer())
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        result = components.BoardEventStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        data['id'] = self.params['id']
        if data['event_date']:
            data['event_date'] = datetime.strptime(data['event_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
        else:
            data['event_date'] = datetime.now().strftime("%Y-%m-%d")
        return components.BoardEventStore(self.get_container()).update(data)


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.BoardEventStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/board/detail/%s/event/list' % (self.params['board_id']))
