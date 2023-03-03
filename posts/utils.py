from django.core.mail import send_mail
from django.core.paginator import Paginator

from posts.models import Item, Tasks

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


def notification(tasks, name):
    if tasks.status.task_status_description == "RELEASED" and tasks.item != "":
        subject = (f'{tasks.event_root}_{tasks.tow}_{tasks.siq} got approved status')
        e_message = (f'{tasks.item} has been relesed. MBOM ver: {tasks.item.bom_ver} ROUT ver: {tasks.item.rout_ver}\n'
                     f'*********************************************************\n'
                     f'{tasks.text}\n'
                     f'<http://meet.vertexaero.space/task/{tasks.id}>\n'
                     f'{name}\n'
                     f'*********************************************************\n'
                     f'This is automatically generated notification. Do not reply to it')
        e_from = 'o.zagryazkin@vertex.aero'
        e_to = ['tasks.person.email','a.osetrov@vertex.aero', 'd.kazyonnykh@vertex.aero', 'a.voinov@vertex.aero']         
    else:
        subject = (f'{tasks.event_root}_{tasks.tow}_{tasks.siq} has been changed')
        e_message = (f'status: {tasks.status}\n'
                     f'due:{tasks.completed_date}\n'
                     f'*******************************************************\n'
                     f'{tasks.text}\n'
                     f'<http://meet.vertexaero.space/task/{tasks.id}>\n'
                     f'{name}\n'
                     f'*******************************************************\n'
                     f'This is automatically generated notification. Do not reply to it')
        e_from = 'o.zagryazkin@vertex.aero'
        e_to = [tasks.person.email, 'a.osetrov@vertex.aero', 's.efimova@vertex.aero', 'a.voinov@vertex.aero']
    send_mail(
        subject,
        e_message,
        e_from,
        e_to,
        fail_silently=False
    )

