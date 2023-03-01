from django.urls import path

from . import views

app_name = 'nonconformance'
urlpatterns = [
    path('dcpcreate/', views.dcp_create, name='dcp_create'),
    path('dcplist/', views.dcp_list, name='dcp_list'),
    path('dcpdetail/<int:dcp_id>', views.dcp_detail, name='dcp_detail'),
    path('dcpcomment/<int:dcp_id>', views.dcp_send_back, name='send_back'),
    path('dcpedit/<int:dcp_id>', views.dcp_edit, name='dcp_edit'),
    path('rptcreate/<int:dcp_id>', views.rpt_create, name='rpt_create'),
    path('rptdetail/<int:rpt_id>', views.rpt_detail, name='rpt_detail'),
    path('dcprelations/<int:dcp_id>', views.dcp_relations, name='dcp_relations'),
    path('changestatus/<int:dcp_id>', views.dcp_change_status, name='dcp_change_status'),
    path('rptchangestatus/<int:rpt_id>', views.rpt_change_status, name='rpt_change_status'),
    path('rptdereview/<int:rpt_id>', views.rpt_de_review, name='rpt_de_review'),
    path('rptoawclosure/<int:rpt_id>', views.rpt_oaw_closure, name='rpt_oaw_closure'),
    path('dcpotherreason/<name>', views.dcp_other_reason, name='dcp_other_reason'),
]
