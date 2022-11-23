from django.contrib import admin

from django.contrib.auth.models import Group

from accounts.models import User, Profile, Bank, Notification

# unregister Group models
admin.site.unregister(Group)

# register User models
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Bank)
admin.site.register(Notification)