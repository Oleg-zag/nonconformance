import time

import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.core.paginator import Paginator
from schedule import every, repeat

from .models import Currency, Item, Tasks

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


def currency_value():
    DOLLAR_RUB = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
    DIRHAM = 'https://www.google.com/search?q=дирхам+к+рублю&ei=_G8HZOmzFJPbrgTozp6AAQ&oq=lbh%5Bfv+к+рублю&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQARgAMgcIABCxAxBDMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKOgoIABBHENYEELADOgcIABCwAxBDOgYIABAHEB46DQgAEAcQHhDxBBAKECo6CAgAEAcQHhAKOgoIABAHEB4QChAqOg0IABAIEAcQHhDxBBAKOgcIABANEIAEOggIABAeEA0QDzoICAAQBRAeEA06DAgAEA0QgAQQRhCCAjoKCAAQDRCABBCxA0oECEEYAFCGEFi1MmD1R2gCcAF4AIABigGIAcEJkgEDNy41mAEAoAEByAEKwAEB&sclient=gws-wiz-serp'
    EVRO = 'https://www.google.com/search?q=евро+к+рублю&ei=EHAHZIm6HM2GwPAP8pW82A0&ved=0ahUKEwiJgt3tp8r9AhVNAxAIHfIKD9sQ4dUDCA8&uact=5&oq=евро+к+рублю&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIMCAAQsQMQQxBGEIICMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOgoIABBHENYEELADOgcIABCwAxBDOgYIABAHEB46BAgAEEM6CAgAEAcQHhAKOgcIABANEIAEOggIABAFEB4QDToKCAAQgAQQDRCxAzoHCAAQgAQQDToGCAAQHhANSgQIQRgAUKAFWP4_YMhGaAVwAXgAgAHcAYgB2gqSAQYxMi4xLjGYAQCgAQHIAQrAAQE&sclient=gws-wiz-serp'
    CNY = 'https://www.google.com/search?q=юань+к+рублю&ei=dHIHZPD8KpS7rgSTwrWIAw&ved=0ahUKEwjwhtWRqsr9AhWUnYsKHRNhDTEQ4dUDCA8&uact=5&oq=юань+к+рублю&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIQCAAQgAQQsQMQgwEQRhCCAjIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoKCAAQRxDWBBCwAzoNCAAQRxDWBBDJAxCwAzoICAAQkgMQsAM6BwgAELADEEM6BAgAEEM6BwgAEIAEEAo6DAgAEOoCELQCEEMYAToOCAAQ6gIQtAIQChBDGAE6CggAELEDEIMBEEM6EQguEIAEELEDEIMBEMcBENEDOhEILhCDARDHARCxAxDRAxCABDoUCC4QgAQQsQMQgwEQxwEQ0QMQ1AI6CwgAEIAEELEDEIMBOggIABCABBCxAzoFCAAQsQM6DwgAELEDEIMBEEMQRhCCAkoECEEYAFDLBFi_NWDBOWgCcAF4BIABjQGIAeIRkgEFMTMuMTCYAQCgAQGwAQrIAQrAAQHaAQQIARgH&sclient=gws-wiz-serp'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    full_page = requests.get(DOLLAR_RUB, headers=headers)
    full_page_dir = requests.get(DIRHAM, headers=headers)
    full_page_evro = requests.get(EVRO, headers=headers)
    full_page_cny = requests.get(CNY, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    soup_dir = BeautifulSoup(full_page_dir.content, 'html.parser')
    soup_evro = BeautifulSoup(full_page_evro.content, 'html.parser')
    soup_cny = BeautifulSoup(full_page_cny.content, 'html.parser')
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    convert_dir = soup_dir.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    convert_evro = soup_evro.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    convert_cny = soup_cny.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})

    return Currency.objects.create(
        currency_usd=convert[0].text,
        currency_aed=convert_dir[0].text,
        currency_eur=convert_evro[0].text,
        currency_cnr=convert_cny[0].text,
    )


schedule.every(1).minutes.do(currency_value)
