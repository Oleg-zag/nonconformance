from xml.etree.ElementTree import Comment

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from posts.constant import (CM, DE, DOEPSEWIS, DOFS, DOMP, DOPWD, DOSTR,
                            DOSTRS, HEAD, LEAD, ME, MELEAD, MEMNG, MEPLANER,
                            OAW, PE, PM, PME, SE, SUPER, TE, VTXPOME, VTXPOMG,
                            VTXPOMP, VTXPOQA, VTXPOSC,
                            VTXPOSF, SENTFORDEREVIEW)
from posts.models import Company, Profile, User

from .forms import (CommentForm, DCPChangeStatusForm, DCPEditForm, DCPForm,
                    OtherForm,
                    PRTCreateForm, RPTChangeStatusForm, RPTDEReviewForm, RPTOAWClosureForm)
from .models import DCP, RPT, Comment, NNstatus, PRTProcessStatus
from .utils import apply_paginator

import datetime


@login_required
def dcp_create(request):
    name = request.user
    form = DCPForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        dcp = form.save(commit=False)
        name_syllable_1 = 'DCP'
        company_name = Profile.objects.get(user=name.id).company
        name_syllable_2 = Company.objects.get(name=company_name).shot_name
        name_syllable_3 = timezone.now().strftime("%y")
        name_syllable_1_2_3 = f'{name_syllable_1}-{name_syllable_2}-{name_syllable_3}'
        nn_name_count = len(DCP.objects.filter(nn_name__startswith=name_syllable_1_2_3)) + 1
        name = f'{name_syllable_1_2_3}-{nn_name_count:03}'
        dcp.nn_name = name
        dcp.applicant = Profile.objects.get(user=request.user)
        dcp.nn_status = NNstatus.objects.get(nn_status="INITIATED")
        if dcp.reason == "Other":
            redirect('nonconformance:dcp_other_reason', name)
           # dcp_other_reason(request, name)
        dcp.save()
        form.save_m2m()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/create_dcp.html', {'form': form})


@login_required
def dcp_edit(request, dcp_id):
    name = request.user
    dcp_detail = DCP.objects.get(id=dcp_id)
    form = DCPEditForm(
        request.POST or None,
        instance=dcp_detail,
        files=request.FILES or None,
    )
    if form.is_valid():
        dcp = form.save(commit=False)
        dcp.applicant = Profile.objects.get(user=name.id)
        dcp.nn_status = NNstatus.objects.get(nn_status="INITIATED")
        dcp.save()
        form.save_m2m()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/edit_dcp.html', {'form': form})


@login_required
def dcp_assign(request, dcp_id):
    dcp_detail = DCP.objects.get(id=dcp_id)
    form = DCPimpactForm(
        request.POST or None,
        instance=dcp_detail,
        files=request.FILES or None,
    )
    if form.is_valid():
        dcp = form.save(commit=False)
        dcp.save()
        form.save_m2m()
        return redirect('nonconformance:dcp_detail')
    return render(request, 'nonconformance/assign_dcp.html', {'form': form})


@login_required
def dcp_list(request):
    '''Output list of nonconformance'''
    nn_list = DCP.objects.all()
    rpt_list = RPT.objects.all()
    page_obj = apply_paginator(nn_list, request)
    context = {
        'page_obj': page_obj,
        'rpt_list': rpt_list,
    }
    return render(request, 'nonconformance/dcp_list.html', context)


@login_required
def dcp_detail(request, dcp_id):
    '''Nonconformance details'''
    dcp = DCP.objects.get(id=dcp_id)
    cdo = Profile.objects.get(department="DESIGN OFFICE", role="HEAD")
    comments = Comment.objects.filter(dcp_id=dcp)
    rpts = RPT.objects.filter(dcp_id=dcp)
    context = {
        'cdo': cdo,
        'rpts': rpts,
        'dcp_detail': dcp,
        'comments': comments,
        'dcpflag': 'dcpflag',
    }
    return render(request, 'nonconformance/dcpdetail.html', context)


def dcp_other_reason(request, dcp_name):
    form = OtherForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        otherrerason = form.save(commit=False)
        otherrerason.dcp = dcp_name
        otherrerason.save()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/dcp_comment.html', {'form': form})


@login_required
def dcp_send_back(request, dcp_id):
    DCP.objects.filter(id=dcp_id).update(
        nn_status=NNstatus.objects.get(nn_status='SEND BACK')
    )
    form = CommentForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        dcp = form.save(commit=False)
        dcp.dcp = DCP.objects.get(id=dcp_id)
        dcp.save()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/dcp_comment.html', {'form': form})


@login_required
def dcp_change_status(request, dcp_id):
    form = DCPChangeStatusForm(
        request.POST or None,
        instance=DCP.objects.get(id=dcp_id),  
        files=request.FILES or None,
    )
    if form.is_valid():
        dcp = form.save(commit=False)
        if dcp.nn_status == "SEND BACK":
            dcp_send_back(request, dcp_id)
        dcp.save()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/dcp_change_status.html', {'form': form})


@login_required
def rpt_change_status(request, rpt_id):
    form = RPTChangeStatusForm(
        request.POST or None,
        instance=RPT.objects.get(id=rpt_id),
        files=request.FILES or None,
    )
    if form.is_valid():
        rpt = form.save(commit=False)
        if rpt.rpt_process_status == PRTProcessStatus.objects.get(
                rpt_process_status="SENT FOR DE REVIEW"):
            rpt.oaw = Profile.objects.get(user=request.user)
            rpt.oaw_date = datetime.date.today()
            rpt.do_date_receipt = datetime.date.today()
        rpt.save()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/rpt_change_status.html', {'form': form})


@login_required
def rpt_de_review(request, rpt_id):
    form = RPTDEReviewForm(
        request.POST or None,
        instance=RPT.objects.get(id=rpt_id),
        files=request.FILES or None,
    )
    if form.is_valid():
        rpt = form.save(commit=False)
        rpt.rpt_process_status = PRTProcessStatus.objects.get(
            rpt_process_status="SENT FOR OAW REVIEW")
        rpt.do_date = datetime.date.today()
        rpt.do = Profile.objects.get(user=request.user)
        rpt.save()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/rpt_de_review.html', {'form': form})


@login_required
def rpt_oaw_closure(request, rpt_id):
    form = RPTOAWClosureForm(
        request.POST or None,
        instance=RPT.objects.get(id=rpt_id),
        files=request.FILES or None,
    )
    if form.is_valid():
        rpt = form.save(commit=False)
        rpt.rpt_process_status = PRTProcessStatus.objects.get(
            rpt_process_status="CLOSURE")
        rpt.hoaw_date = datetime.date.today()
        rpt.hoaw = Profile.objects.get(user=request.user)
        rpt.save()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/rpt_de_review.html', {'form': form})


@login_required
def rpt_create(request, dcp_id):
    form = PRTCreateForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        rpt = form.save(commit=False)
        rpt.dcp = DCP.objects.get(id=dcp_id)
        name_syllable_1 = 'RPT'
        user = rpt.dispatched_to
        department = Profile.objects.get(user=user.id)
        if department.department == CM:
            name_syllable_2 = 'CM'
        elif department.department == DOSTR or DOPWD or DOMP:
            name_syllable_2 = "DO"
        elif department.department == VTXPOME:
            name_syllable_2 = "PO"
        name_syllable_3 = timezone.now().strftime("%y")
        name_syllable_1_2_3 = f'{name_syllable_1}-{name_syllable_2}-{name_syllable_3}'
        rpt_name_count = len(RPT.objects.filter(rpt_name__startswith=name_syllable_1_2_3)) + 1
        rpt.rpt_name = f'{name_syllable_1_2_3}-{rpt_name_count:03}'
        # rpt.rpt_status = NNstatus.objects.get(nn_status='INITIATED')
        rpt.rpt_process_status = PRTProcessStatus.objects.get(rpt_process_status="DISPATCHED")
        rpt_last = RPT.objects.all().count()
        rpt.id = rpt_last + 1
        rpt.save()
        form.save_m2m()
        return redirect('nonconformance:dcp_detail', dcp_id=dcp_id)
    return render(request, 'nonconformance/create_rpt.html', {'form': form})


@login_required
def rpt_detail(request, rpt_id):
    '''RPT details'''
    rpt_detail = get_object_or_404(RPT, id=rpt_id)
    dcp_detail = rpt_detail.dcp
    context = {
        'rpt_detail': rpt_detail,
        'dcp_detail': dcp_detail,
        'rptflag': 'rptflag',
    }
    return render(request, 'nonconformance/rptdetail.html', context)


@login_required
def dcp_relations(request, dcp_id):
    dcp_detail = get_object_or_404(DCP, id=dcp_id)
    rpt_list = RPT.objects.filter(dcp=dcp_id)
    context = {
        'dcp_detail': dcp_detail,
        'rpt_list': rpt_list,
        'dcp': 'флажок dcp',
    }
    return render(request, 'nonconformance/dcprelations.html', context)