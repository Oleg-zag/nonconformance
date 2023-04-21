
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.core.paginator import Paginator
from django.shortcuts import render
from django.template.loader import get_template
import datetime

from .models import Tasks, User

from django.db.models import Count, Q

POSTS_PAR_PAGE = 200

def apply_paginator(posts, request):
    paginator = Paginator(posts, POSTS_PAR_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def status_count(item_msn, msn):
    task = []
    ready_to_work = 0
    in_work = 0
    ready_for_check = 0
    on_hold = 0
    in_check = 0
    released = 0
    checked = 0
    cancelled = 0
    total = 0
    for items in item_msn:
        total += 1
        tasks = Tasks.objects.filter(item=items.item.id).latest('id')
        if tasks.status.task_status_description == 'RTWORK':
            ready_to_work = ready_to_work + 1
        if tasks.status.task_status_description == 'INWORK':
            in_work = in_work + 1
        if tasks.status.task_status_description == 'RFCHECK':
            ready_for_check = ready_for_check + 1
        if tasks.status.task_status_description == 'ONHOLD':
            on_hold = on_hold + 1
        if tasks.status.task_status_description == 'IN CHECK':
            in_check = in_check + 1
        if tasks.status.task_status_description == 'RELEASED':
            released = released + 1
        if tasks.status.task_status_description == 'CHECKED':
            checked = checked + 1
        if tasks.status.task_status_description == 'CANCELED':
            cancelled = cancelled + 1
        task.append(tasks)
    if msn == 1:
        context = {
            'ready_to_work': ready_to_work,
            'in_work': in_work,
            'ready_for_check': ready_for_check,
            'on_hold': on_hold,
            'in_check': in_check,
            'released': released,
            'checked': checked,
            'cancelled': cancelled,
            'msn000': 'msn000',
            'task': task,
            'total': total,
            'item_msn0000': item_msn,
        }
        return(context)
    elif msn == 2:
        context = {
            'ready_to_work': ready_to_work,
            'in_work': in_work,
            'ready_for_check': ready_for_check,
            'on_hold': on_hold,
            'in_check': in_check,
            'released': released,
            'checked': checked,
            'cancelled': cancelled,
            'msn0002': 'msn0002',
            'task': task,
            'total': total,
            'item_msn0000': item_msn,
        }
        return(context)


def notification(tasks, user):
    task_details = tasks.ttask.select_related('task_s')
    task_set = tasks
    context = {'tasks': task_details,
               'task_set': task_set,
               }
    if tasks.status.task_status_description == "RELEASED" and tasks.tow == 'JCC':
        subject = (f'{tasks.event_root}_{tasks.tow}_{tasks.siq} got approved status')
        text_content = (f'{tasks.item} has been relesed. MBOM ver: {tasks.item.bom_ver} ROUT ver: {tasks.item.rout_ver}\n'
                    f'*********************************************************\n'
                    f'{tasks.text}\n'
                    f'<http://meet.vertexaero.space/task/{tasks.id}>\n'
                    f'{user}\n'
                    f'*********************************************************\n'
                    f'This is automatically generated notification. Do not reply to it')
        e_from = 'zagryazkin@gmail.com'
        e_to = ['tasks.person.email','a.osetrov@vertex.aero', 'd.kazyonnykh@vertex.aero', 'a.voinov@vertex.aero']
        html_content = get_template('posts/user_task_for_email.html').render(context)
    else:
        subject = (f'{tasks.event_root}_{tasks.tow}_{tasks.siq} has been changed')
        text_content = (f'status: {tasks.status}\n'
                        f'due:{tasks.completed_date}\n'
                        f'*******************************************************\n'
                        f'{tasks.text}\n'
                        f'<http://meet.vertexaero.space/task/{tasks.id}>\n'
                        f'{user}\n'
                        f'*******************************************************\n'
                        f'This is automatically generated notification. Do not reply to it')
        e_from = 'zagryazkin@gmail.com'
        e_to = [tasks.person.email, 'a.osetrov@vertex.aero', 's.efimova@vertex.aero', 'a.voinov@vertex.aero']
        html_content = get_template('posts/user_task_for_email.html').render(context)
        # e_html_message = render('posts/task_detail_for_email.html', context={'task': tasks})
    # msg = EmailMultiAlternatives(
    #     subject,
    #     text_content,
    #     e_from,
    #     e_to,
    # )
    # msg.attach_alternative(html_content, "text/html")
    # msg.send(fail_silently=False)
        msg = EmailMessage(
            subject,
            html_content,
            e_from,
            e_to,
        )
        msg.content_subtype = "html"
        msg.send(fail_silently=False)


def task_user_application(user, tasks):
    tasks_fiasco = tasks.filter(~Q(status__task_status_description='RELEASED') & Q(completed_date__lte=datetime.datetime.now()))
    tasks_inwork = tasks.filter(~Q(status__task_status_description='RELEASED') & Q(completed_date__gte=datetime.datetime.now()))
    context = {'tasks': tasks,
               'tasks_fiasco': tasks_fiasco,
               'tasks_inwork': tasks_inwork,
               }
    subject = ('TASKS APPLIED TO YOU')
    text_content = ('Be aware the following tasks applied to you')
    e_from = 'e3eadb5b-ed3a-4190-9aa5-566fbba84598'
    e_to = [user.email]
    html_content = get_template('posts/user_applied_task_for_email.html').render(context)
    # msg = EmailMultiAlternatives(
    #     subject,
    #     text_content,
    #     e_from,
    #     e_to,
    # )
    # msg.attach_alternative(html_content, "text/html")
    # msg.send(fail_silently=False)
    html_content = get_template('posts/user_applied_task_for_email.html').render(context)
    msg = EmailMessage(
        subject,
        html_content,
        e_from,
        e_to,
    )
    msg.content_subtype = "html"
    msg.send(fail_silently=False)


def task_user_application_2(user, tasks):
    tasks_fiasco = tasks.filter(~Q(status__task_status_description='RELEASED') & Q(completed_date__lte=datetime.datetime.now()))
    tasks_inwork = tasks.filter(~Q(status__task_status_description='RELEASED') & Q(completed_date__gte=datetime.datetime.now()))
    context = {'tasks': tasks,
               'tasks_fiasco': tasks_fiasco,
               'tasks_inwork': tasks_inwork,
               }
    subject = ('TASKS APPLIED TO YOU')
    e_from = 'e3eadb5b-ed3a-4190-9aa5-566fbba84598'
    e_to = [user.email]
    html_content = get_template('posts/user_applied_task_for_email.html').render(context)
    msg = EmailMessage(
        subject,
        html_content,
        e_from,
        e_to,
    )
    msg.content_subtype = "html"
    msg.send(fail_silently=False)


def tasks_fiasco(tasks):
    person = User.objects.annotate(fiasco=Count('tasks', filter=(~Q(tasks__status__description='RELEASED') & Q(tasks__completed_date__lte=datetime.datetime.now()))))
    context = {'tasks': tasks}
    subject = ('FIASCO TASKS')
    text_content = ('Be aware the following tasks pass the DUE')
    e_from = 'app.debugmail.io'
    e_to = ['o.zagryazkin@vertex.aero']
    html_content = get_template(
        'posts/fiasco_task_for_email.html').render(context)
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        e_from,
        e_to,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
    # )
    # send_mail(
    #     subject,
    #     e_message,
    #     e_from,
    #     e_to,
    #     fail_silently=False,
    #     e_html_message,
    # )
