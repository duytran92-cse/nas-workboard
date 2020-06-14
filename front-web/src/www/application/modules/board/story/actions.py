from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
from application.modules.common import page_contexts, actions as common_actions
from notasquare.urad_web.widgets import BaseWidget
from application.common import registry

class List(actions.crud.ListAction):
    def create_page_context(self):
        self.params['submenu'] = 'story'
        if 'stage_id' in self.params:
            self.params['submenu'] = 'stage-%s' % (self.params['stage_id'])
        if 'assignee_id' in self.params:
            self.params['submenu'] = 'assignee-%s' % (self.params['assignee_id'])
        if 'category_id' in self.params:
            self.params['submenu'] = 'category-%s' % (self.params['category_id'])
        if 'is_your_story' in self.params:
            self.params['submenu'] = 'your_story'
        self.params['page_title'] = 'Story'
        return board_components.BoardFullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="checkbox m-b-15" style="margin-top:0px; margin-bottom: 0px !important">'
            html += '    <input type="hidden" id="story-id-%s" value=%s>' % (row['id'], row['id'])
            html += '    <input type="hidden" id="board-id-%s" value=%s>' % (row['id'], row['board_id'])
            html += '   <label>'
            html += '      <input type="checkbox" name="checkbox-story" id="%s" class="input">' % (row['id'])
            html += '      <i class="input-helper"></i>'
            html += '   </label>'
            html += '</div>'


            return html
        def render_cell_manager(self, table, row):
            return row['manager_label']
        def render_cell_name(self, table, row):
            row_html = '<div><span>%s</span> <span class="pull-right">' % (row['name'])
            for val in row['tags']:
                row_html+= '<a href="#" data-placement="top" data-trigger="hover" data-toggle="popover" data-original-title="%s" data-content="%s"' % (val['info']['name'], val['info']['value'])
                row_html+=' data-type="info" style="color: %s; font-size:16px;padding-right:2px"> <i class="%s" id="%s"></i> </a>' % (row['text_color'], val['icon'], val['id'])
            row_html+="</span></div>"
            return row_html
        def render_row(self, table, row):
            row_html = '<tr style="cursor:pointer;background-color:'+ row['bg_color']+'; color: '+ row['text_color']+'">'
            if 'id' in row:
                row_html = '<tr val="'+ str(row['id'])+'" style="cursor:pointer;background-color:'+ row['bg_color']+'; color: '+ row['text_color']+'">'
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
            all_stage = []
            board_id = ''
            rows_html = ''
            for row in table.data:
                all_stage = row['all_stage']
                board_id  = row['board_id']
                rows_html += self.render_row(table, row)
            context['rows_html'] = rows_html
            context['all_stage'] = all_stage
            context['board_id'] = board_id
            return template.render(context)
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Story')
        table.set_subtitle('List of stories')
        table.create_button('create', '/board/detail/%s/story/create' % (self.params['board_id']), 'Add', 'btn btn-sm bgm-cyan waves-effect')
        table.create_button('bulk-delete', '#', 'Delete', 'btn btn-sm btn-danger waves-effect')
        table.create_column('id', 'ID', '5%', sortable=True)
        table.create_column('name', 'Name', '45%')
        table.create_column('assignee_label', 'Assignee', '15%', sortable=True)
        table.create_column('board_category_label', 'Category', '15%')
        table.create_column('board_stage_label', 'Stage', '15%')
        table.create_column('actions', '', '5%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.template = 'workboard/board/story/table.html'
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Text', colspan=12)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        table_form_data['board_id'] = self.params['board_id']
        if 'stage_id' in self.params:
            table_form_data['stage_id'] = self.params['stage_id']
        if 'category_id' in self.params:
            table_form_data['category_id'] = self.params['category_id']
        if 'assignee_id' in self.params:
            table_form_data['assignee_id'] = self.params['assignee_id']
        if 'is_your_story' in self.params:
            table_form_data['user_id'] = registry.USER['user_id']
        return components.BoardStoryStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number=0)
    def view_list_page(self):
        page_context = self.create_page_context()
        table = self.create_table()
        self.populate_table(table)
        page_context.add_widget(table)
        return HttpResponse(page_context.render())
    def create_stage_side_widget(self):
        widget = components.StageSideWidget()
        widget.build(self.container, self.params)
        return widget
    def create_category_side_widget(self):
        widget = components.CategorySideWidget()
        widget.build(self.container, self.params)
        return widget

class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        self.params['submenu'] = 'story'
        self.params['page_title'] = 'Update story'
        return board_components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Story')
        form.add_field(widgets.field.Combobox('board_category_id', choices=board_category_components.BoardCategoryStore(self.get_container()).populate_combobox(self.params['board_id'])))
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Combobox('assignee_id',choices=user_components.UserStore(self.get_container()).populate_combobox(), blank=True))
        form.add_field(widgets.field.Texteditor('description'))
        form.add_field(widgets.field.Combobox('manager_id', choices=user_components.UserStore(self.get_container()).populate_combobox(), blank=True))
        form.add_field(widgets.field.Combobox('board_stage_id', choices=board_stage_components.BoardStageStore(self.get_container()).populate_combobox(self.params['board_id'])))
        form.renderer = components.StoryFormRenderer()
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('texteditor', renderers.widgets.field.TexteditorRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        form.renderer.set_field_renderer('multiple_choice', renderers.widgets.field.MultipleChoiceRenderer())
        form.renderer.set_field_renderer('list', renderers.widgets.field.ListRenderer())
        return form
    def load_form(self, form):
        result = components.BoardStoryStore(self.get_container()).get(self.params['id'])
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        data['id'] = self.params['id']
        data['user_id'] = registry.USER['user_id']
        return components.BoardStoryStore(self.get_container()).update(data)
    def GET(self):
        page_context = self.create_page_context()
        form = self.create_form()
        self.load_form(form)
        page_context.add_widget(form)

        page_context.add_side_widget(self.create_tag_side_widget())
        page_context.add_side_widget(self.create_comment_side_widget())
        page_context.add_side_widget(self.create_rating_side_widget())
        page_context.add_side_widget(self.create_log_side_widget())

        return HttpResponse(page_context.render())
    def create_comment_side_widget(self):
        widget = components.CommentSideWidget()
        widget.build(self.container, self.params)
        return widget

    def create_log_side_widget(self):
        widget = components.LogSideWidget()
        widget.build(self.container, self.params)
        return widget

    def create_tag_side_widget(self):
        widget = components.TagSideWidget()
        widget.build(self.container, self.params)
        return widget


    def create_rating_side_widget(self):
        widget = components.RatingSideWidget()
        widget.build(self.container, self.params)
        return widget
    def handle_on_success(self, messages):
        return HttpResponseRedirect('/board/detail/%s/story/list' % (self.params['board_id']))


class Create(actions.crud.CreateAction):
    def create_page_context(self):
        self.params['submenu'] = 'story'
        self.params['page_title'] = 'Create story'
        return board_components.BoardFullPageContext(self.params, self.container)
    def create_form(self):
        form = widgets.form.Form()
        form.set_title('Story')
        form.add_field(widgets.field.Combobox('board_category_id', choices=board_category_components.BoardCategoryStore(self.get_container()).populate_combobox(self.params['board_id'])))
        form.add_field(widgets.field.Textbox('name'))
        form.add_field(widgets.field.Combobox('assignee_id', choices=user_components.UserStore(self.get_container()).populate_combobox(), blank=True))
        form.add_field(widgets.field.Texteditor('description'))
        form.add_field(widgets.field.Combobox('manager_id', choices=user_components.UserStore(self.get_container()).populate_combobox(), blank=True))
        form.add_field(widgets.field.Combobox('board_stage_id', choices=board_stage_components.BoardStageStore(self.get_container()).populate_combobox(self.params['board_id'])))
        form.renderer = components.StoryFormRenderer()
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
        data['user_id'] = registry.USER['user_id']
        return components.BoardStoryStore(self.get_container()).create(data)
    def handle_on_success(self, messages):
        return HttpResponseRedirect('/board/detail/%s/story/list' % (self.params['board_id']))

class ChangeStage(common_actions.BaseAction):
    def POST(self):
        rs = components.BoardStoryStore(self.get_container()).change_stage(self.params)
        return JsonResponse(rs)

class BulkDelete(common_actions.BaseAction):
    def POST(self):
        rs = components.BoardStoryStore(self.get_container()).bulk_delete(self.params)
        return JsonResponse(rs)

class DeleteTag(common_actions.BaseAction):
    def POST(self):
        rs = components.BoardStoryStore(self.get_container()).delete_tag(self.params['id'])
        return JsonResponse(rs)

class AddComment(common_actions.BaseAction):
    def POST(self):
        rs = components.BoardStoryStore(self.get_container()).add_cmt(self.params)
        return JsonResponse(rs)

class AddTag(common_actions.BaseAction):
    def POST(self):
        rs = components.BoardStoryStore(self.get_container()).add_tag(self.params)
        return JsonResponse(rs)

class UpdateRating(common_actions.BaseAction):
    def POST(self):
        rs = components.BoardStoryStore(self.get_container()).update_rating(self.params)
        return JsonResponse(rs)
