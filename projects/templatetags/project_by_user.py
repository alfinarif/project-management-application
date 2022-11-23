from django import template
from projects.models import ProjectSubmission
from django.db.models import Q

register = template.Library()

@register.filter
def total_project(user):
    projects = ProjectSubmission.objects.filter(Q(project__worker=user) & Q(project__status='done'))
    if projects.exists():
        return projects.count()
    else:
        return 0