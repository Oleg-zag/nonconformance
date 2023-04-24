from xml.etree.ElementTree import Comment

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from posts.constant import (CM, DE, DOEPSEWIS, DOFS, DOMP, DOPWD, DOSTR,
                            DOSTRS, HEAD, LEAD, ME, MELEAD, MEMNG, MEPLANER,
                            OAW, PE, PM, PME, SE, SENTFORDEREVIEW, SUPER, TE,
                            VTXPOME, VTXPOMG, VTXPOMP, VTXPOQA, VTXPOSC,
                            VTXPOSF)
from posts.models import Company, Profile, User

from .forms import (CommentForm, DCPChangeStatusForm, DCPEditForm, DCPForm,
                    OtherForm, PRTCreateForm, RPTChangeStatusForm,
                    RPTDEReviewForm, RPTOAWClosureForm, TDCForm, ORFForm, DCPUpdateForm)
from .models import DCP, RPT, Comment, NNstatus, PRTProcessStatus, TDC, ORF
from .utils import apply_paginator, tdc_creation, orf_creation
from datetime import date



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
        company_name=Profile.objects.get(user=name.id).company
        if company_name == Company.objects.get(name='VERTEX AERO SRL') and Profile.objects.get(user=name.id).department != "VTX MANUFACTURING ENGINEERIN":
            name_syllable_2 = "DO"
        else:
            name_syllable_2 = company_name.shot_name
        name_syllable_3 = timezone.now().strftime("%y")
        name_syllable_1_2_3 = f'{name_syllable_1}-{name_syllable_2}-{name_syllable_3}'
        name = f'{name_syllable_1_2_3}-XXX'
        dcp.nn_name = name
        dcp.applicant = Profile.objects.get(user=request.user)
        dcp.nn_status = NNstatus.objects.get(nn_status="INITIATED")
        dcp.save()
        form.save_m2m()
        dcp.save()
        if dcp.reason == "Other":
            return redirect('nonconformance:dcp_other_reason', name)
        else:
            return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/create_dcp.html', {'form': form})


@login_required
def dcp_other_reason(request, name):
    form = OtherForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        otherrerason = form.save(commit=False)
        otherrerason.dcp = name
        otherrerason.save()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/dcp_reason_form.html', {'form': form})


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
        tdc_name_syllable_1 = 'TDC'
        orf_name_syllable_1 = 'ORF'
        tdc_name_syllable_2 = timezone.now().strftime("%y")
        orf_name_syllable_2 = timezone.now().strftime("%y")
        tdc_name_syllable_1_2 = f'{tdc_name_syllable_1}-{tdc_name_syllable_2}'
        orf_name_syllable_1_2 = f'{orf_name_syllable_1}-{orf_name_syllable_2}'
        tdc_name_count = len(
            TDC.objects.filter(
                tdc_name__startswith=tdc_name_syllable_1_2)) + 1
        orf_name_count = len(
            ORF.objects.filter(
                orf_name__startswith=orf_name_syllable_1_2)) + 1
        tdc = f'{tdc_name_syllable_1_2}-{tdc_name_count:03}'
        orf = f'{orf_name_syllable_1_2}-{orf_name_count:03}'
        TDC.objects.create(tdc_name=tdc, tdc_rev='A', dcp=dcp.id)
        ORF.objects.create(orf_name=orf, orf_rev='A', dcp=dcp.id)
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
    rpts = RPT.objects.filter(dcp_id=dcp)
    cdo = Profile.objects.get(department="DESIGN OFFICE", role="HEAD")
    comments = Comment.objects.filter(dcp_id=dcp)
    if TDC.objects.filter(dcp=dcp_id).exists() and ORF.objects.filter(dcp=dcp_id).exists():
        tcp_detail = TDC.objects.get(dcp=dcp_id)
        orf_detail = ORF.objects.get(dcp=dcp_id)
        context = {
            'tcp_detail': tcp_detail,
            'orf_detail': orf_detail,
            'cdo': cdo,
            'rpts': rpts,
            'dcp_detail': dcp,
            'comments': comments,
            'dcpflag': 'dcpflag',
        }
    else:
        context = {
            'rpts': rpts,
            'cdo': cdo,
            'dcp_detail': dcp,
            'comments': comments,
            'dcpflag': 'dcpflag',
        }
    return render(request, 'nonconformance/dcpdetail.html', context)


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
        if dcp.nn_status.nn_status == "SEND BACK":
            dcp_send_back(request, dcp_id)
        elif dcp.nn_status.nn_status == "READY FOR DIAP":
            tdc = tdc_creation(request, dcp_id)
            if tdc is not None:
                TDC.objects.create(tdc_name=tdc, tdc_rev='A', dcp=dcp)
            orf = orf_creation(request, dcp_id)
            if orf is not None:
                ORF.objects.create(orf_name=orf, orf_rev='A', dcp=dcp)
        elif dcp.nn_status.nn_status == "RPT DISPATCHED":
            dcp.cdo_signature = request.user
        dcp.save()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/dcp_change_status.html', {'form': form})


@login_required
def dcp_process(request, dcp_id):
    name = request.user
    dcp_detail = DCP.objects.get(id=dcp_id)
    name_syllable_1 = 'DCP'
    company_name = Profile.objects.get(user=name.id).company
    if company_name == Company.objects.get(name='VERTEX AERO SRL') and Profile.objects.get(user=name.id).department != "VTX MANUFACTURING ENGINEERIN":
        name_syllable_2 = "DO"
    else:
        name_syllable_2 = company_name.shot_name
    name_syllable_2 = Company.objects.get(name=company_name).shot_name
    name_syllable_3 = timezone.now().strftime("%y")
    name_syllable_1_2_3 = f'{name_syllable_1}-{name_syllable_2}-{name_syllable_3}'
    nn_name_count = len(DCP.objects.filter(
        nn_name__startswith=name_syllable_1_2_3).exclude(nn_name__contains="XXX")) + 1
    name = f'{name_syllable_1_2_3}-{nn_name_count:03}'
    dcp_detail.nn_name = name
    dcp_detail.nn_status = NNstatus.objects.get(nn_status="READY FOR DIAP")
    dcp_detail.save()
    rpts = RPT.objects.filter(dcp_id=dcp_id)
    if TDC.objects.filter(dcp=dcp_id).exists() and ORF.objects.filter(dcp=dcp_id).exists():
        tcp_detail = TDC.objects.get(dcp=dcp_id)
        orf_detail = ORF.objects.get(dcp=dcp_id)
        context = {
            'tcp_detail': tcp_detail,
            'orf_detail': orf_detail,
            'rpts': rpts,
            'dcp_detail': dcp_detail,
            'dcpflag': 'dcpflag',
        }
    else:
        context = {
            'rpts': rpts,
            'dcp_detail': dcp_detail,
            'dcpflag': 'dcpflag',
        }
    return render(request, 'nonconformance/dcpdetail.html', context)


@login_required
def rpt_change_status(request, rpt_id):
    dcp_detail = RPT.objects.get(id=rpt_id).dcp
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
            rpt.oaw_date = date.today()
            rpt.do_date_receipt = date.today()
        rpt.save()
        rpt_process_status = PRTProcessStatus.objects.get(rpt_process_status='SENT FOR DE REVIEW')
        if RPT.objects.filter(dcp=dcp_detail).count() == RPT.objects.filter(dcp=dcp_detail, rpt_process_status=rpt_process_status).count():
            dcp_detail.nn_status = "READY FOR RPT DO EVALUATION"
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/rpt_change_status.html', {'form': form})


@login_required
def rpt_send_for_de_review(request, rpt_id):
    dcp_detail= RPT.objects.get(id=rpt_id).dcp
    rpt = RPT.objects.get(id=rpt_id)
    rpt_process_status = PRTProcessStatus.objects.get(rpt_process_status='SENT FOR DE REVIEW')
    rpt.rpt_process_status = rpt_process_status
    rpt.save()
    if RPT.objects.filter(dcp=dcp_detail).count() == RPT.objects.filter(dcp=dcp_detail, rpt_process_status=rpt_process_status).count():
        dcp_detail.nn_status = NNstatus.objects.get(nn_status="READY FOR RPT DO EVALUATION")
        dcp_detail.save()
    return redirect('nonconformance:dcp_list')


@login_required
def rpt_de_review(request, rpt_id):
    dcp_detail = RPT.objects.get(id=rpt_id).dcp
    form = RPTDEReviewForm(
        request.POST or None,
        instance=RPT.objects.get(id=rpt_id),
        files=request.FILES or None,
    )
    if form.is_valid():
        rpt = form.save(commit=False) 
        rpt.rpt_process_status = PRTProcessStatus.objects.get(
            rpt_process_status="SENT FOR OAW REVIEW")
        rpt.do_date = date.today()
        rpt.do = Profile.objects.get(user=request.user)
        rpt.save()
        rpt_process_status = PRTProcessStatus.objects.get(rpt_process_status='SENT FOR OAW REVIEW')
        if RPT.objects.filter(dcp=dcp_detail).count() == RPT.objects.filter(dcp=dcp_detail, rpt_process_status=rpt_process_status).count():
             dcp_detail.nn_status = NNstatus.objects.get(
                nn_status="RPT DO EVALUATED")
             dcp_detail.save()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/rpt_de_review.html', {'form': form})


@login_required
def rpt_oaw_closure(request, rpt_id):
    dcp_detail = RPT.objects.get(id=rpt_id).dcp
    rpt_process_status = PRTProcessStatus.objects.get(rpt_process_status='CLOSURE') 
    form = RPTOAWClosureForm(
        request.POST or None,
        instance=RPT.objects.get(id=rpt_id),
        files=request.FILES or None,
    )
    if form.is_valid():
        rpt = form.save(commit=False)
        rpt.rpt_process_status = PRTProcessStatus.objects.get(
            rpt_process_status="CLOSURE")
        rpt.hoaw_date = date.today()
        rpt.hoaw = Profile.objects.get(user=request.user)
        rpt.save()
        if RPT.objects.filter(dcp=dcp_detail).count() == RPT.objects.filter(dcp=dcp_detail, rpt_process_status=rpt_process_status).count():
            dcp_detail.nn_status = NNstatus.objects.get(
                nn_status="RPT CLOSED")
            dcp_detail.save()
        return redirect('nonconformance:dcp_list')
    return render(request, 'nonconformance/rpt_de_review.html', {'form': form})


@login_required
def rpt_create(request, dcp_id):
    form = PRTCreateForm(
        request.POST or None,
        files=request.FILES or None,
    )
    dcp = DCP.objects.get(id=dcp_id)
    if form.is_valid():
        rpt = form.save(commit=False)
        rpt.dcp = dcp
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
        tdc = tdc_creation(request, dcp_id)
        if tdc is not None:
            TDC.objects.create(tdc_name=tdc, tdc_rev='A', dcp=dcp)
        orf = orf_creation(request, dcp_id)
        if orf is not None:
            ORF.objects.create(orf_name=orf, orf_rev='A', dcp=dcp)
        return redirect('nonconformance:dcp_detail', dcp_id=dcp_id)
    return render(request, 'nonconformance/create_rpt.html', {'form': form})


@login_required
def rpt_detail(request, rpt_id):
    '''RPT details'''
    rpt_detail = get_object_or_404(RPT, id=rpt_id)
    dcp_detail = rpt_detail.dcp
    rpt_list = RPT.objects.filter(dcp=dcp_detail)
    if TDC.objects.filter(dcp=dcp_detail).exists() and ORF.objects.filter(dcp=dcp_detail).exists():
        tcp_detail = TDC.objects.get(dcp=dcp_detail)
        orf_detail = ORF.objects.get(dcp=dcp_detail)
        context = {
            'tcp_detail': tcp_detail,
            'rpt_detail': rpt_detail,
            'dcp_detail': dcp_detail,
            'orf_detail': orf_detail,
            'rpts': rpt_list,
            'rptflag': True,
        }
    else:
        context = {
            'rpt_detail': rpt_detail,
            'dcp_detail': dcp_detail,
            'rpts': rpt_list,
            'rptflag': True,
        }
    return render(request, 'nonconformance/rptdetail.html', context)


@login_required
def dcp_relations(request, dcp_id):
    dcp_detail = get_object_or_404(DCP, id=dcp_id)
    rpt_list = RPT.objects.filter(dcp=dcp_id)
    tcp_detail = TDC.objects.get(dcp=dcp_id)
    context = {
        'dcp_detail': dcp_detail,
        'rpt_list': rpt_list,
        'tcp_detail': tcp_detail,
        'dcpflag': True,
    }
    return render(request, 'nonconformance/dcprelations.html', context)


@login_required
def tcp_detail(request, tcp_id):
    tcp_detail = TDC.objects.get(id=tcp_id)
    dcp_detail = tcp_detail.dcp
    rpt_list = RPT.objects.filter(dcp=dcp_detail)
    orf_detail = ORF.objects.get(dcp=dcp_detail)
    context = {
        'dcp_detail': dcp_detail,
        'rpts': rpt_list,
        'tcp_detail': tcp_detail,
        'orf_detail': orf_detail,
        'tcpflag': True
    }
    return render(request, 'nonconformance/tcp_detail.html', context)


@login_required
def tcp_update(request, tcp_id):
    tcp_detail = get_object_or_404(TDC, id=tcp_id)
    dcp_detail = tcp_detail.dcp
    orf_detail = ORF.objects.get(dcp=dcp_detail)
    rpt_list = RPT.objects.filter(dcp=dcp_detail)
    form = TDCForm(
        request.POST or None,
        instance=tcp_detail,
        files=request.FILES or None,
    )
    if form.is_valid():
        tcd = form.save(commit=False)
        if tcd.tcp_process_status == "PREPARED":
           tcp_detail.prepared_oaw = Profile.objects.get(user=request.user)
           tcp_detail.date_oaw = date.today()
        if tcd.tcp_process_status == "APPROVED":
           orf_detail.HDO = Profile.objects.get(user=request.user)
           dcp_detail.nn_status = NNstatus.objects.get(nn_status="TDC APPROVED")
           tcp_detail.date_hoaw = date.today()
        dcp_detail.save()
        tcd.save()
        form.save()
        return redirect('nonconformance:dcp_list')
    context = {
        'orf_detail': orf_detail,
        'dcp_detail': dcp_detail,
        'rpts': rpt_list,
        'tcp_detail': tcp_detail,
        'tcpflag': True,
        'form': form,
    }
    return render(request, 'nonconformance/tcp_edit.html', context)


@login_required
def orf_detail(request, orf_id):
    orf_detail = ORF.objects.get(id=orf_id)
    dcp_detail = orf_detail.dcp
    rpt_list = RPT.objects.filter(dcp=dcp_detail)
    tcp_detail = TDC.objects.get(dcp=dcp_detail)
    context = {
        'dcp_detail': dcp_detail,
        'rpts': rpt_list,
        'orf_detail': orf_detail,
        'orfflag': True,
        'tcp_detail': tcp_detail,
    }
    return render(request, 'nonconformance/orf_detail.html', context)


@login_required
def orf_update(request, orf_id):
    orf_detail = get_object_or_404(ORF, id=orf_id)
    dcp_detail = orf_detail.dcp
    rpt_list = RPT.objects.filter(dcp=dcp_detail)
    tcp_detail = TDC.objects.get(dcp=dcp_detail)
    form = ORFForm(
        request.POST or None,
        instance=orf_detail,
        files=request.FILES or None,
    )
    if form.is_valid():
        orf = form.save(commit=False)
        if orf.orf_process_status == "PREPARED":
           orf_detail.prepared_oaw = Profile.objects.get(user=request.user)
           dcp_detail.nn_status = NNstatus.objects.get(nn_status="ORF PREPARED")
        if orf.orf_process_status == "APPROVED":
           orf_detail.HDO = Profile.objects.get(user=request.user)
           dcp_detail.nn_status = NNstatus.objects.get(nn_status="ORF APPROVED")
        dcp_detail.save()
        orf.save()
        form.save()
        return redirect('nonconformance:dcp_list')
    context = {
        'dcp_detail': dcp_detail,
        'rpts': rpt_list,
        'orf_detail': orf_detail,
        'tcp_detail': tcp_detail,
        'tcpflag': True,
        'form': form,
    }
    return render(request, 'nonconformance/orf_edit.html', context)


@login_required
def dcp_approve(request, dcp_id):
    name = request.user
    dcp_detail = DCP.objects.get(id=dcp_id)
    form = DCPUpdateForm(
        request.POST or None,
        instance=dcp_detail,
        files=request.FILES or None,
    )
    if form.is_valid():
        dcp = form.save(commit=False)
        dcp.oaw = Profile.objects.get(user=name.id)
        dcp.nn_status = NNstatus.objects.get(nn_status="CLOSED")
        dcp.oaw_date = date.today()
        dcp.save()
        form.save_m2m()
        return redirect('nonconformance:dcp_list')
    context = {
        'dcp_detail': dcp_detail,
        'form': form,

    }
    return render(request, 'nonconformance/dcp_update.html', context)