from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from .models import DCP, RPT, NNstatus, PRTProcessStatus, PRTreviewStatus

# Register your models here.


class DCPResource(resources.ModelResource):
    class Meta:
        model = DCP


class DCPAdmin(ImportExportActionModelAdmin):
    resource_class = DCPResource
    list_display = [field.name for field in DCP._meta.fields if field.name != 'id']


class NNstatusResource(resources.ModelResource):
    class Meta:
        model = NNstatus


class NNstatusAdmin(ImportExportActionModelAdmin):
    resource_class = NNstatusResource
    list_display = [field.name for field in NNstatus._meta.fields if field.name != 'id']


class PRTResource(resources.ModelResource):
    class Meta:
        model = RPT


class RPTAdmin(ImportExportActionModelAdmin):
    resource_class = PRTResource
    list_display = [field.name for field in RPT._meta.fields if field.name != 'id']


class PRTreviewStatusResource(resources.ModelResource):
    class Meta:
        model = PRTreviewStatus


class PRTreviewStatusAdmin(ImportExportActionModelAdmin):
    resource_class = PRTreviewStatusResource
    list_display = [field.name for field in PRTreviewStatus._meta.fields if field.name != 'id']


class PRTProcessStatusResource(resources.ModelResource):
    class Meta:
        model = PRTProcessStatus


class PRTProcessStatusAdmin(ImportExportActionModelAdmin):
    resource_class = PRTProcessStatusResource
    list_display = [field.name for field in PRTProcessStatus._meta.fields if field.name != 'id']


admin.site.register(DCP, DCPAdmin)
admin.site.register(NNstatus, NNstatusAdmin)
admin.site.register(RPT, RPTAdmin)
admin.site.register(PRTreviewStatus, PRTreviewStatusAdmin)
admin.site.register(PRTProcessStatus, PRTProcessStatusAdmin)
