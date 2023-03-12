import smtplib
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django import template
from django.utils import timezone

from posts.models import Currency

register = template.Library()


def year(request):
    """Добавляет переменную с текущим годом."""
    today = timezone.now()
    return {
        'year': today.year
    }


def currency(request):
    """Добавляет переменную с валютой."""
    carranciesval = Currency.objects.last()
    return {'currency_aed': carranciesval.currency_aed,
            'currency_eur': carranciesval.currency_eur,
            'currency_cnr': carranciesval.currency_cnr,
            'currency_usd': carranciesval.currency_usd,
            }


@register.simple_tag
def warnday(format):
    warnday = datetime.date.today + datetime.timedelta(days=3)
    return warnday.strftime(format)