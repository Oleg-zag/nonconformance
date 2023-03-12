from django.core.paginator import Paginator


POSTS_PAR_PAGE = 200


def apply_paginator(nn_list, request):
    paginator = Paginator(nn_list, POSTS_PAR_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
