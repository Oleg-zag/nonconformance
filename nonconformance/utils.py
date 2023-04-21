from django.core.paginator import Paginator
from django.utils import timezone
from .models import TDC, ORF

POSTS_PAR_PAGE = 200


def apply_paginator(nn_list, request):
    paginator = Paginator(nn_list, POSTS_PAR_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def tdc_creation(request, dcp_id):
    if TDC.objects.filter(dcp=dcp_id).exists():
        return (None)
    tdc_name_syllable_1 = 'TDC'
    tdc_name_syllable_2 = timezone.now().strftime("%y")
    tdc_name_syllable_1_2 = f'{tdc_name_syllable_1}-{tdc_name_syllable_2}'
    tdc_name_count = len(
        TDC.objects.filter(
            tdc_name__startswith=tdc_name_syllable_1_2)) + 1
    return(f'{tdc_name_syllable_1_2}-{tdc_name_count:03}')


def orf_creation(request, dcp_id):
    if ORF.objects.filter(dcp=dcp_id).exists():
        return (None)
    orf_name_syllable_1 = 'ORF'
    orf_name_syllable_2 = timezone.now().strftime("%y")
    orf_name_syllable_1_2 = f'{orf_name_syllable_1}-{orf_name_syllable_2}'
    orf_name_count = len(
        ORF.objects.filter(
            orf_name__startswith=orf_name_syllable_1_2)) + 1
    return(f'{orf_name_syllable_1_2}-{orf_name_count:03}')
