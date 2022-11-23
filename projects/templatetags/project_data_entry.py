from django import template
from projects.models import Issues
from django.db.models import Q

register = template.Library()

@register.filter
def total_data_entry(project):
    data_entry = Issues.objects.filter(Q(project=project))

    total = 0
    for entry in data_entry:
        total += int(entry.total_data_entry_today)
    return total