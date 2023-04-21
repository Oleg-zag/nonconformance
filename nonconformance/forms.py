from tkinter import Radiobutton
from django import forms
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget

from .models import DCP, RPT, Comment, NNstatus, OtherRerason
from .models import TDC, ORF


class DCPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        def new_label_from_dcp(self, obj):
            return obj.svgpreview

        super().__init__(*args, **kwargs)
        # self.fields['nn_status'].empty_label = "status not selected"
        # self.fields['applicability'].empty_label = "prototype not selected"
        # self.fields['reason'].widgets = forms.CheckboxSelectMultiple(),

    class Meta:
        model = DCP
        fields = (
            'part_number',
            'applicability', 'reason', 'description_of_change',
            'description_of_change_image',
            'solutions', 'annex',
        )
        labels = {
            'part_number': 'Part Number',
            'reason': 'Reason',
            'description_of_change': 'Description of change',
            'description_of_change_image': 'Description Image',
            'solutions': 'Solution / Corretive Action Proposed / Impacted areas',
            'annex': 'Annex',
        }

        css = {
            'all': (
                '/static/admin/css/widgets.css',
            )
        }
        js = [
            '/admin/jsi18n/',
            '/static/admin/js/core.js',
        ]


class DCPOpenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['impact_areas_proposal'].empty_label = "not selected"

    class Meta:
        model = DCP
        fields = (
            'impact_areas_proposal', 'doa_decision',
            'request_evaluation', 'annex',
        )
        labels = {
            'impact_areas_proposal': 'Impact Area Proposal',
            'doa_decision': 'DOA desition',
            'request_evaluation': 'Request Evaluation',
            'annex': 'Annex',
        }
        css = {
            'all': (
                '/static/admin/css/widgets.css',
            )
        }
        js = [
            '/admin/jsi18n/',
            '/static/admin/js/core.js',
        ]


class DCPEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['nn_status'].empty_label = "status not selected"
        # self.fields['applicability'].empty_label = "prototype not selected"
        self.fields['reason'].widgets = forms.CheckboxSelectMultiple(),

    class Meta:
        model = DCP
        fields = (
            'part_number',
            'applicability', 'reason', 'description_of_change',
            'description_of_change_image',
            'solutions', 'annex',
        )
        labels = {
            'part_number': 'Part number',
            'reason': 'Reason',
            'description_of_change': 'Description of change',
            'description_of_change_image': 'Description Image',
            'solutions': 'Solution / Corretive Action Proposed / Impacted areas',
            'annex': 'Annex',
        }
        css = {
            'all': (
                '/static/admin/css/widgets.css',
            )
        }
        js = [
            '/admin/jsi18n/',
            '/static/admin/js/core.js',
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        labels = {
            'comment': 'Enter comment',
        }


class PRTCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['nn_status'].empty_label = "status not selected"
        # self.fields['applicability'].empty_label = "prototype not selected"
        # self.fields['reason'].widgets = forms.CheckboxSelectMultiple(),

    class Meta:
        model = RPT
        fields = ('dispatched_to',
                  'description',
                  'description_image')
        labels = {'dispatched_to': 'Dispatch to',
                  'description': 'Description',
                  'description_image': 'image'}
        css = {
            'all': (
                '/static/admin/css/widgets.css',
            )
        }
        js = [
            '/admin/jsi18n/',
            '/static/admin/js/core.js',
        ]


class DCPChangeStatusForm(forms.ModelForm):
    class Meta:
        model = DCP
        fields = ('nn_status',)
        labels = {'nn_status': 'Select nonconformance process status'}


class RPTChangeStatusForm(forms.ModelForm):
    class Meta:
        model = RPT
        fields = ('rpt_process_status',)
        labels = {'rpt_process_status': 'Select RPT process status'}


class RPTDEReviewForm(forms.ModelForm):
    class Meta:
        model = RPT
        fields = ('review_note', 'rpt_review_status',)
        labels = {
            'review_note': ' Add CVE/DO review note',
            'rpt_review_status': 'Accept or Reject',
        }


class RPTOAWClosureForm(forms.ModelForm):
    class Meta:
        model = RPT
        fields = ('oaw_note',)
        labels = {
            'oaw_note': 'OAW closure note',
        }


class OtherForm(forms.ModelForm):
    class Meta:
        model = OtherRerason
        fields = (
            'reason',
        )
        labels = {
            'reason': 'define a reason of DCP',
        }


class TDCForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = TDC
        fields = ('incorporate', 'doc_number_to_change',
                  'description_of_change', 'reason_of_change',
                  'organinizational', 'technical_not_substantial',
                  'minor', 'major', 'fcd_mmel', 'note', 'tcp_process_status',
                  )
        lebels = {'incorporate': 'incorporate or NOT',
                  'doc_number_to_change': 'document/part numbers to change',
                  'doc_number_changed': 'document/part numbers changed/issued',
                  'description_of_change': 'desxcription of change',
                  'reason_of_change': 'reason of change',
                  'organinizational': 'organizational',
                  'technical_not_substantional': 'technical not substantional',
                  'minor': 'minor',
                  'major': 'major',
                  'fcd_mmel': 'fcd mmel',
                  'note': 'note',
                  }
        widgets = {
            'incorporate': forms.CheckboxInput(attrs={'type': 'checkbox'}),
            'fcd_mmel': forms.Select(attrs={'type': 'checkbox'}),
        }


class ORFForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = ORF
        fields = ('orf_evaluation_status',
                  'description',
                  'orf_process_status')


class DCPUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = DCP
        fields = ('doa_decision',
                  'request_evaluation',
                  )