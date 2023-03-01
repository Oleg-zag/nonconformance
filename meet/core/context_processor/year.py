from datetime import datetime

from django import template
from django.utils import timezone

register = template.Library()

def year(request):
    """Добавляет переменную с текущим годом."""
    today = timezone.now()
    return {
        'year': today.year
    }

@register.simple_tag
def warnday(format):
    warnday = datetime.date.today + datetime.timedelta(days=3)
    return warnday.strftime(format)