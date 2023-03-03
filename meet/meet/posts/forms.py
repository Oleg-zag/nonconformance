from django import forms
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget

from .models import Comment, Import, Post, Status, Task, Tasks
from .widget import DatePickerInput, DateTimePickerInput, TimePickerInput


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['group'].empty_label = "Группа не выбрана"

    class Meta:
        model = Post
        fields = ('text', 'image')
        help_texts = {
            'group': 'Related group',
            'text': 'post text'
        }
        labels = {
            'text': 'Post text',
            'group': 'Group',
            'image': 'Picture'
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        labels = ('Comment',)


class TasksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].empty_label = "status not selected"
        self.fields['action'].empty_label = "action not selected"
        self.fields['item'].empty_label = "item not selected"
        self.fields['msn'].empty_label = "prototype not selected"
        self.fields['person'].empty_label = "engineer not selected"
        self.fields['tow'].empty_label = "type of work not selected"
        self.fields['completed_date'].widget = DatePickerInput()

    class Meta:
        model = Tasks
        fields = (
            'tow',
            'item', 'text', 'project', 'group',
            'completed_date',
            'planned_time',
            'status', 'person', 'action', 'msn',
        )
        help_text = {
            'tow': 'select type of work',
            'item': 'select item',
            'status': 'select status',
            'person': 'select person',
            'action': 'select action',
            'msn': 'select prototype',
            'projec': 'list of projects',
        }
        labels = {
            'tow': 'Тype Of Work',
            'item': 'Item',
            'status': 'Status',
            'person': 'Enginner',
            'action': 'Action',
            'msn': 'Prototype',
            'text': 'Note',
            'project': 'list of projects',
        }
        css = {
            'all': (
                '/static/admin/css/widgets.css',
            )
        }
        js = [
            '/admin/jsi18n/',
            '/static/admin/js/core.js',
            ]
        widgets = {
            'completed_date': DatePickerInput(),
            # 'my_time_field' : TimePickerInput(),
            # 'completed_date' : DateTimePickerInput(),
        }


class TaskForm(forms.ModelForm):
    #text = forms.Textarea()
    #status = forms.ModelChoiceField(queryset=Status.objects.all())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].empty_label = "status not selected"
        self.fields['person'].empty_label = "engineer not selected"
        # self.fields['completed_date'].widget = DatePickerInput()

    class Meta:
        model = Task
        fields = (
            'text',
            'status', 'person',
            'time_consume',
            'image',
        )
        labels = {
            'status': 'Status',
            'person': 'Engineer',
            'text': 'Note',
            'completed_date': 'ECD',
            'time_consume': 'time',
        }


class TaskDuedateForm(forms.ModelForm):
    class Meta:
        model = Task

        fields = (
            'completed_date',
            'text',
            'status', 'person',
            'completed_date',
            'image',
            'time_consume',
        )
        labels = {
            'status': 'Status',
            'person': 'Engineer',
            'text': 'Note',
            'completed_date': 'Due date',
            'time_consume': 'time',
        }
        widgets = {
            'completed_date': DatePickerInput()
        }

