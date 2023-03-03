from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path(
        'posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('follow/', views.follow_index, name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow',
    ),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/', views.tasks_list, name='tasks_list'),
    path('task/action/<int:action_id>/', views.action_posts, name='action_list'),
    path('createtask/', views.tasks_create, name='tasks_create'),
    path('edittask/<int:task_id>', views.task_edit, name='tasks_edit'),
    path('jclistmsn0000/', views.item_list_msn0000, name='item_list_msn0000'),
    path('jclistmsn0002/', views.item_list_msn0002, name='item_list_msn0002'),
    path('itemtasks/<int:item_id>', views.constrained_tasks, name='constrained_tasks'),
    path('item_list_msn_status/<int:msn_id>/<int:status_id>/', views.item_list_msn_status,
         name='item_list_msn_status'),
]
