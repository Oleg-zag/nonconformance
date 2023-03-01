from django.contrib.auth import get_user_model
from django.db import models

from posts.models import Ebom0000, Profile, Prototype

User = get_user_model()

LEN_OF_TEXT = 15
MDR = 'MDR'
PP = 'PP'
AW = "Airworthiness"
FI = 'Functional improvement'
CuR = 'Customer request'
PD = 'Procurement difficulties'
CoR = 'Cost reduction'
PPI = 'Production process improvement'
OTH = 'Other'
RJ = 'REJECTED'
AC = 'ACCEPTED'
OP = 'OPEN'
CL = 'CLOSED'
IN = 'INITIATED'
DISPATCHED = 'DISPATCHED'
SENTFORDEREVIEW = 'SENT FOR DE REVIEW'
RPTRECEVEIDBYDE = 'RPT RECEIVED BY DE/CVE'
READYFORCLOSURE = 'SENT FOR OAW REVIEW'
CLOSURE = 'CLOSURE'
RR = 'READY FOR RPT'
RD = 'RPT DISPATCHED'
RC = 'RPT CLOSED'
SB = 'SEND BACK'
REASON_LIST = [
    (AW, 'Airworthiness'),
    (FI, 'Functional improvement'),
    (CuR, 'Customer request'),
    (PD, 'Procurement difficulties'),
    (CoR, 'Cost reduction'),
    (PPI, 'Production process improvement'),
    (OTH, 'Other'),
]
REQUEST_EVALUATION = [
    (RJ, 'REJECTED'),
    (AC, 'ACCEPTED'),
]
NONCONFORMANCE_STATUS = [
    (SB, 'SENT BACK'),
    (RC, 'RPTs CLOSED'),
    (RD, 'RPTs DISPATCHED'),
    (RR, 'READY FOR RPT'),
    (IN, 'INITIATED'),
    (OP, 'OPENED'),
    (CL, 'CLOSED'),
]
RPT_PROCESS_STATUS =[
    (DISPATCHED, 'DISPATCHED'),
    (SENTFORDEREVIEW, 'SENT FOR DE REVIEW'),
    (RPTRECEVEIDBYDE, 'RPT RECEIVED BY DE/CVE'),
    (READYFORCLOSURE, 'SENT FOR OAW REVIEW'),
    (CLOSURE, 'CLOSURE'),
]
NONCONFORMANCE_TYPE = [
    (PP, 'PP'),
    (MDR, 'MDR'),
]


class PRTProcessStatus(models.Model):
    rpt_process_status = models.CharField(
        max_length=40,
        null=False,
        blank=False,
        choices=RPT_PROCESS_STATUS,
    )

    def __str__(self):
        return self.rpt_process_status


class PRTreviewStatus(models.Model):
    rpt_review_status = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=REQUEST_EVALUATION,
    )

    def __str__(self):
        return self.rpt_review_status


class NNstatus(models.Model):
    nn_status = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        choices=NONCONFORMANCE_STATUS,
    )

    def __str__(self):
        return self.nn_status


class DCP(models.Model):
    nn_name = models.CharField(max_length=20)
    nn_status = models.ForeignKey(
        NNstatus,
        models.CASCADE,
        null=False,
        blank=False,
    )
    part_number = models.ManyToManyField(
        Ebom0000,
        null=True,
        blank=True,
    )
    applicability = models.ManyToManyField(
        Prototype,
        blank=False,
        null=False,
    )
    reason = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        choices=REASON_LIST,
    )
    description_of_change = models.TextField()
    description_of_change_image = models.ImageField(
        'Picture',
        upload_to='posts/',
        blank=True,
        null=True,
    )
    solutions = models.TextField()
    applicant = models.ForeignKey(
        Profile,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='app',
    )
    applicant_date = models.DateField(
        auto_now_add=True,
    )
    impact_areas_proposal = models.ManyToManyField(
        Profile,
        null=True,
        blank=True,
        related_name='i_a_p',
    )
    cdo_signature = models.ForeignKey(
        User,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='c_d_o',
    )
    doa_decision = models.TextField(
        null=True,
        blank=True,
    )
    request_evaluation = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=REQUEST_EVALUATION,
    )
    oaw = models.ForeignKey(
        Profile,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='o_a_w',
    )
    annex = models.FileField(
        upload_to='posts/',
        blank=True,
    )


class NN(models.Model):
    nn_name = models.CharField(max_length=20)
    nn_status = models.ForeignKey(
        NNstatus,
        models.CASCADE,
        null=False,
        blank=False,
    )
    part_number = models.ManyToManyField(
        Ebom0000,
        null=True,
        blank=True,
    )
    pp_status = models.BooleanField(
        null=False,
        blank=False,
    )
    pp_date = models.DateField(
        auto_now_add=True,
    )
    vertex_doc = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    purchase_order = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    drawing_issue = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    batch_qty = models.IntegerField(
        null=False,
        blank=False,
    )
    defective_qty = models.IntegerField(
        null=False,
        blank=False,
    )
    manufacture_po = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    department = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    model = models.ManyToManyField(
        Prototype,
        blank=False,
        null=False,
    )
    defect_descriptions = models.TextField()
    defect_descriptions_image = models.ImageField(
        'Picture',
        upload_to='posts/',
        blank=True,
        null=True,
    )
    mdr_pn = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    mdr_lot = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    inspector = models.ForeignKey(
        Profile,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='insp',
    )
    inspector_date = models.ForeignKey(
        Profile,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='inspdate',
    )
    defect_cause = models.TextField()
    defect_cause_image = models.ImageField(
        'Picture',
        upload_to='posts/',
        blank=True,
        null=True,
    )
    ca_to_remove_case = models.BooleanField(
        blank=True,
        null=True,
    )
    complete_before = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    pp_initiater_signature = models.ForeignKey(
        Profile,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='ppsignature',
    )
    solutions = models.TextField()
    initiater = models.ForeignKey(
        Profile,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='initiater',
    )
    date = models.DateField(
        auto_now_add=True,
    )
    doa_decision = models.TextField(
        null=True,
        blank=True,
    )
    request_evaluation = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=REQUEST_EVALUATION,
    )
    oaw = models.ForeignKey(
        Profile,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='ow',
    )
    annex = models.FileField(
        upload_to='posts/',
        blank=True,
    )


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(
        User,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='com',
    )
    dcp = models.ForeignKey(
        DCP,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='com',
    )
    date = models.DateField(
        auto_now_add=True,
    )
    nn = models.ForeignKey(
        NN,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='com',
    )


class RPT(models.Model):
    dcp = models.ForeignKey(
        DCP,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='dcp',
    )
    nn = models.ForeignKey(
        NN,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='nn',
    )
    rpt_name = models.CharField(max_length=20)
    rpt_review_status = models.ForeignKey(
        PRTreviewStatus,
        models.DO_NOTHING,
        null=True,
        blank=True,
    )
    rpt_status = models.ForeignKey(
        NNstatus,
        models.CASCADE,
        null=True,
        blank=True,
        related_name='rpt',
    )
    rpt_process_status = models.ForeignKey(
        PRTProcessStatus,
        models.DO_NOTHING,
        null=True,
        blank=True,
    )
    applicant_date = models.DateField(
        auto_now_add=True,
    )
    dispatched_to = models.ForeignKey(
        User,
        models.CASCADE,
        blank=True,
        null=True,
        related_name='dis',
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    description_image = models.ImageField(
        'Picture',
        upload_to='posts/',
        blank=True,
        null=True,
    )
    review_note = models.TextField(
        blank=True,
        null=True,
    )
    oaw_date = models.DateField(
        blank=True,
        null=True,
    )
    do_date_receipt = models.DateField(
        blank=True,
        null=True,
    )
    do_date = models.DateField(
        blank=True,
        null=True,
    )
    hoaw_date = models.DateField(
        blank=True,
        null=True,
    )
    oaw = models.ForeignKey(
        Profile,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='oaw',
    )
    do_receipt = models.ForeignKey(
        Profile,
        models.CASCADE,
        blank=True,
        null=True,
        related_name='d_r',
    )
    do = models.ForeignKey(
        Profile,
        models.CASCADE,
        blank=True,
        null=True,
        related_name='do',
    )
    hoaw = models.ForeignKey(
        Profile,
        models.CASCADE,
        blank=True,
        null=True,
        related_name='hoaw',
    )
    oaw_note = models.TextField(
        blank=True,
        null=True,
    )


class OtherRerason(models.Model):
    reason = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    slug = models.SlugField(unique=False)
    dcp = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
