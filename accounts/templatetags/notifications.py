from django import template
from accounts.models import Notification
from django.db.models import Q


register = template.Library()

@register.filter
def notification_leader(user):
    notifications = Notification.objects.filter(Q(to_leader=user) & Q(is_active=True) & Q(is_seen=False)).order_by('-id')
    if notifications.exists():
        return notifications
    else:
        return None

@register.filter
def notification_worker(user):
    notifications = Notification.objects.filter(Q(to_worker=user) & Q(is_active=True) & Q(is_seen=False)).order_by('-id')
    if notifications.exists():
        return notifications
    else:
        return None


@register.filter
def notification_leader_count(user):
    notifications = Notification.objects.filter(Q(to_worker=user) & Q(is_active=True) & Q(is_seen=False)).order_by('-id')
    if notifications.exists():
        return notifications.count()
    else:
        return 0


@register.filter
def notification_worker_count(user):
    notifications = Notification.objects.filter(Q(to_worker=user) & Q(is_active=True) & Q(is_seen=False)).order_by('-id')
    if notifications.exists():
        return notifications.count()
    else:
        return 0