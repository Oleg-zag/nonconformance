from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm, TaskDuedateForm, TaskForm, TasksForm
from .models import (Action, Follow, Group, Item, Post, Projectlist,
                     ReportMsn0000, Task, Tasks, User)
from .utils import apply_paginator, notification, status_count


@login_required
def index(request):
    """Выводит главную страницу"""
    post_list = Post.objects.select_related('group', 'author').all()
    page_obj = apply_paginator(post_list, request)
    context = {
        'index': 'флажок index',
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Выводит все посты сообщества"""
    group = get_object_or_404(Group, slug=slug)
    posts = group.post.select_related('group', 'author')
    page_obj = apply_paginator(posts, request)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_edit = 'is_edit'
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.id)
    context = {
        'is_edit': is_edit,
        'form': form,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    '''Создание комментария'''
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


def post_detail(request, post_id):
    """Выводит шаблон поста пользователя"""
    post_detail = get_object_or_404(
        Post.objects.select_related(), pk=post_id)
    form = CommentForm(request.POST or None)
    comments = post_detail.comments.all()
    context = {
        'post_detail': post_detail,
        'comments': comments,
        'form': form
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    page_obj = apply_paginator(post_list, request)
    context = {
        'follow': 'флажок follow',
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    following = get_object_or_404(User, username=username)
    follower = get_object_or_404(User, username=request.user)
    if following == follower:
        return redirect('posts:profile', username=username)
    obj_create = Follow.objects.get_or_create(
        author=following, user=request.user)
    if not obj_create:
        return redirect('posts:profile', username=username)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    following = get_object_or_404(User, username=username)
    obj_exists = Follow.objects.filter(
        author=following,
        user=request.user,
    )
    if obj_exists.exists() is True:
        obj_exists.delete()
    return redirect('posts:profile', username=username)


@login_required
def task_detail(request, task_id):
    """Выводит шаблон c деталями задания"""
    task = get_object_or_404(Tasks, pk=task_id)
    task_detail = task.ttask.select_related('task_s')
    context = {
        'task': task,
        'task_detail': task_detail,
    }
    return render(request, 'posts/task_detail.html', context)


def action_posts(request, action_id):
    """List of tasks related to the action"""
    action = get_object_or_404(Action, pk=action_id)
    posts = Tasks.objects.select_related(
        'status', 'person', 'action', 'msn').filter(action=action_id)
    page_obj = apply_paginator(posts, request)
    context = {
        'action': action,
        'page_obj': page_obj,
    }
    return render(request, 'posts/action_list.html', context)


@login_required
def tasks_list(request):
    """Выводит главную страницу"""
    tasks_list = Tasks.objects.select_related(
        'status', 'person', 'action').all()
    page_obj = apply_paginator(tasks_list, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/tasks_list.html', context)


@login_required
def tasks_create(request):
    name = request.user
    form = TasksForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        tasks = form.save(commit=False)
        if 'ME-VTX-' in tasks.action.name:
            mecount = len(
                Tasks.objects.filter(event_root__startswith='ME')) + 1
            tasks.event_root = f'ME{mecount:08}'
            tasks.siq = '001'
            tasks.save()
            form.save_m2m()
        else:
            event_name = tasks.action.name
            tasks.event_root = event_name.replace('-VTX-', '')
            count_siq = len(Tasks.objects.filter(action=tasks.action))
            tasks.siq = f'{count_siq:03}'
            tasks.save()
            form.save_m2m()
        Task.objects.get_or_create(
            task_name=tasks.event_root,
            siq=tasks.siq,
            tow=tasks.tow,
            completed_date=tasks.completed_date,
            action=tasks.action,
            person=tasks.person,
            status=tasks.status,
            text=(f'{tasks.text}\n'
                  f'{name}'),
            task_s=tasks,
        )
        notification(tasks, request.user)
        return redirect('posts:tasks_list')
    return render(request, 'posts/create_task.html', {'form': form})


@login_required
def task_edit(request, task_id):
    name = request.user
    if request.user.profile.role == "MANUFACTURING ENGINEER MANAGER" or request.user.profile.role == "MANUFACTURING ENGINEER PLANER":
        form = TaskDuedateForm(
            request.POST or None,
            files=request.FILES or None,
        )
    else:
        form = TaskForm(
            request.POST or None,
            files=request.FILES or None,
        )
    if form.is_valid():
        tasks = Tasks.objects.get(id=task_id)
        project = Projectlist.objects.get(id=tasks.project.id)
        task = form.save(commit=False)
        Projectlist.objects.filter(
            id=project.id).update(
               time_left=project.time_left - task.time_consume,
               time_spent=project.time_spent + task.time_consume,
        )
        tasks.time_consume = tasks.time_consume + task.time_consume
        tasks.status = task.status
        tasks.text = (f'{task.text}\n'
                      f'{name}')
        tasks.person = task.person
        if task.completed_date is None:
            tasks.save(update_fields=[
                'status',
                'person',
            ])
            task.task_name = tasks.event_root
            task.tow = tasks.tow
            task.item = tasks.item
            task.action = tasks.action
            task.siq = tasks.siq
            task.task_s = tasks
            task.text = (f'{task.text}\n'
                         f'{name}')
            task.save()
            notification(tasks, request.user)
            tas = Task.objects.all().latest('id')
            tas.completed_date = tasks.completed_date
            tas.save(update_fields=[
                'completed_date'])
            return redirect('posts:tasks_list')
        elif task.completed_date is not None:
            tasks.completed_date = task.completed_date
            tasks.save(update_fields=[
                'status',
                'person',
                'text',
                'completed_date',
            ])
            task.text = (f'{task.text}\n'
                      f'{name}')
            task.task_name = tasks.event_root
            task.tow = tasks.tow
            task.item = tasks.item
            task.action = tasks.action
            task.siq = tasks.siq
            task.task_s = tasks
            notification(tasks, request.user)
            task.save()
            return redirect('posts:tasks_list')
    return render(request, 'posts/edit_task.html', {'form': form})


@login_required
def constrained_tasks(request, item_id):
    items_tasks = Tasks.objects.filter(item=item_id)
    context = {
                'items_tasks': items_tasks,
    }
    return render(request, 'posts/itemtasks.html', context)


@login_required
def item_list_msn0000(request):
    """MSN REPORT 0000"""
    item_msn0000 = ReportMsn0000.objects.filter(msn=1)
    context = status_count(item_msn0000, 1)
    return render(request, 'posts/item_list_msn0000.html', context)


@login_required
def item_list_msn_status(request, msn_id, status_id):
    """MSN REPORT 0000 and status"""
    item_list = ReportMsn0000.objects.filter(msn=msn_id)
    task = Tasks.objects.filter(status=status_id)
        # task.append(tasks)
    context = {
        'item_list': item_list,
        'task': task,
        'status': status_id
    }
    return render(request, 'posts/item_list_msn_status.html', context)

@login_required
def item_list_msn0002(request):
    """MSN REPORT 0002"""
    item_msn0000 = ReportMsn0000.objects.filter(msn=2)
    context = status_count(item_msn0000, 2)
    return render(request, 'posts/item_list_msn0000.html', context)


def profile(request, username):
    """Выводит все посты пользователя"""
    author = get_object_or_404(User, username=username)
    task_list = author.tasks.select_related()
    page_obj = apply_paginator(task_list, request)
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            author=author, user=request.user).exists()
        context = {
            'author': author,
            'page_obj': page_obj,
            'following': following,
        }
    else:
        context = {
            'author': author,
            'page_obj': page_obj,
        }
    return render(request, 'posts/profile.html', context)
