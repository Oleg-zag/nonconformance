from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import ForeignKeyWidget

from .models import (Action, Comment, Company, Ebom0000, Group, Item, Post,
                     Profile, Projectlist, Prototype, ReportMsn0000,
                     Shopeflore, Status, Task, Tasks, Tow)


class ActionResource(resources.ModelResource):
    class Meta:
        model = Action


class ActionAdmin(ImportExportActionModelAdmin):
    resource_class = ActionResource
    list_display = [field.name for field in Action._meta.fields if field.name != 'id']


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class TaskResource(resources.ModelResource):
    class Meta:
        model = Task


class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Task._meta.fields if field.name != 'id']
    list_editable = ('person', 'completed_date', 'status',)


class Ebom0000Resource(resources.ModelResource):
    class Meta:
        model = Ebom0000


class Ebom0000Admin(ImportExportActionModelAdmin):
    resource_class = Ebom0000Resource
    list_display = [field.name for field in Ebom0000._meta.fields if field.name != 'id']
    list_filter = ('title',)
    search_fields = ('title',)


class StatusAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'task_status',
        'task_status_description',
    )
    list_editable = ('task_status', 'task_status_description',)


class PrototypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'msn',)


class TowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tow_name', 'tow_desc')
    list_editable = ('tow_name', 'tow_desc')


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item


class TasksResource(resources.ModelResource):
    class Meta:
        model = Tasks


class TasksAdmin(admin.ModelAdmin):
    resource_class = TaskResource
    list_display = (
         'event_root', 'siq',
         'text', 'date', 'completed_date',
         'status', 'person', 'action', 'msn', 'tow',
    )

        # field.name for field in Tasks._meta.fields if field.name != 'id']


class ItemAdmin(ImportExportActionModelAdmin):
    resource_class = ItemResource
   # list_display = [field.name for field in Item._meta.fields if field.name != 'id']
    list_filter = ('name',)
    autocomplete_fields = ('bom',)


class ShopefloreAdmin(admin.ModelAdmin):
    list_display = (
        'sta', 'sta_name',
    )
    list_editable: ('sta', 'sta_name')


class ProjectlistResource(resources.ModelResource):
    class Meta:
        model = Item


class ProjectlistAdmin(ImportExportActionModelAdmin):
    resource_class = ProjectlistResource
    list_display = [field.name for field in Projectlist._meta.fields if field.name != 'id']


class ReportMsn0000Resource(resources.ModelResource):
    class Meta:
        model = Item


class ReportMsn0000Admin(ImportExportActionModelAdmin):
    resource_class = ReportMsn0000Resource
    list_display = [field.name for field in ReportMsn0000._meta.fields if field.name != 'id']
    search_filter = ('item',)


class GroupResource(resources.ModelResource):
    class Meta:
        model = Group


class GroupAdmin(ImportExportActionModelAdmin):
    resource_class = GroupResource
    list_display = [field.name for field in Group._meta.fields if field.name != 'id']


class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile


class ProfileAdmin(ImportExportActionModelAdmin):
    resource_class = ProfileResource
    list_display = [field.name for field in Profile._meta.fields if field.name != 'id']


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company


class CompanyAdmin(ImportExportActionModelAdmin):
    resource_class = CompanyResource
    list_display = [field.name for field in Company._meta.fields if field.name != 'id']


admin.site.register(Group)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Task, TaskAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(Prototype, PrototypeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Tow)
admin.site.register(Item, ItemAdmin)
admin.site.register(Shopeflore, ShopefloreAdmin)
admin.site.register(Ebom0000, Ebom0000Admin)
admin.site.register(Projectlist, ProjectlistAdmin)
admin.site.register(ReportMsn0000, ReportMsn0000Admin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Company, CompanyAdmin)
