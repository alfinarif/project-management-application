from django.contrib import admin

from projects.models import Categories, Project, Task, Issues, ProjectSubmission

admin.site.register(Categories)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Issues)
admin.site.register(ProjectSubmission)
