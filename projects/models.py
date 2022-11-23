from django.db import models
from django_quill.fields import QuillField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

    
#ToDo: Total Project Done by user
#ToDo: Total Project Record by user
#ToDo: Total Entry by User per week , month, year
#ToDo: Total Project
#ToDo: Total Project Done

# a user can submit single time for a project -> task submission editable valided for the 24 hours




PROJECT_STATUS_CHOICE = (
            ("New", "New"),
            ("Backlog", "Backlog"),
            ("Blocked", "Blocked"),
            ("In Progress", "In Progress"),
            ("Test/Review", "Test/Review"),
            ("Closed", "Closed"),
)

QUOTE_APPROVAL_STATUS = (
            ("REJECTED", "REJECTED"),
            ("DRAFT", "DRAFT"),
            ("APPROVED", "APPROVED"),
)

RATING_SCORE = (
            (1, "1 Star"),
            (2, "2 Star"),
            (3, "3 Star"),
            (4, "4 Star"),
            (5, "5 Star"),
)

RFC_APPROVAL = (
            (1, "Waiting"),
            (2, "Approved"),
            (3, "Rejected"),
            (4, "Cancel"),
)

RFC_IMPACT = (
            (3, "High"),
            (2, "Medium"),
            (1, "Low"),
)

RFC_PRIORITY = (
            (4, "Critical"),
            (3, "High"),
            (2, "Medium"),
            (1, "Low"),
)

RFC_RISK = (
            (5, "Very High"),
            (4, "High"),
            (3, "Moderate"),
            (2, "Low"),
            (1, "None"),
)

RFC_STATUS = (
            (1, "Draft"),
            (2, "Waiting for approval"),
            (3, "Approved"),
            (4, "Started"),
            (5, "Finished"),
            (6, "Rejected"),
)

RFC_TYPE = (
            (4, "Emergency"),
            (3, "High"),
            (2, "Medium"),
            (1, "Low"),
)

WANT_CHOICE = (
    ("0", "Do not want to do"),
            ("1", "Want to do"),
)

ACCEPT_STATUS = (
    ('draft', 'draft'),
    ('decline', 'decline'),
    ('accept', 'accept'),
    ('pending', 'pending'),
            
)

STATUS = (
    ('draft', 'draft'),
    ('stuck', 'Stuck'),
    ('working', 'Working'),
    ('done', 'Done'),
)

DUE = (
            ('on due', 'On Due'),
            ('overdue', 'Overdue'),
            ('done', 'Done'),
)

class Categories(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.name)


class Project(models.Model):
    name = models.CharField(max_length=255) # done
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='projects')# done
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')# done
    worker = models.ManyToManyField(User)# done
    status = models.CharField(max_length=7, choices=STATUS, default=1)# done
    accept_status = models.CharField(max_length=15, choices=ACCEPT_STATUS, default=ACCEPT_STATUS[0])# done
    work_start_date = models.DateField()# done
    work_end_date = models.DateField()# done
    deadline = models.DateField()# done
    project_client_budget = models.IntegerField(default=0)# done
    project_eastemate_cost = models.IntegerField(default=0)# done
    sort_description = models.CharField(max_length=300, blank=False, null=False)# done
    description = QuillField()# done
    complete_per = models.FloatField(max_length=2, blank=True, null=True, validators = [MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False)
    file = models.FileField(upload_to='project_file')
    add_date = models.DateField(auto_now_add=True)
    upd_date = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return (self.name)
    
    @property
    def issues(self):
        return issues_set.all().order_by('-id')

    def project_accept(self, user):
        worker_project = Project.objects.filter(Q(worker=user) & Q(status='stuck', accept_status='accept'))
        return worker_project
    
    def project_pending(self, user):
        worker_project = Project.objects.filter(Q(worker=user) & Q(status='working', accept_status='pending'))
        return worker_project
    
    def project_decline(self, user):
        worker_project = Project.objects.filter(Q(worker=user) & Q(accept_status='decline'))
        return worker_project




class Task(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    worker = models.ManyToManyField(User)
    status = models.CharField(max_length=7, choices=STATUS, default=1)
    due = models.CharField(max_length=7, choices=DUE, default=1)
    description = QuillField()
    deadline = models.DateField()
    is_active = models.BooleanField(default=False)
    complete_per = models.FloatField(max_length=4, blank=True, null=True, validators = [MinValueValidator(0), MaxValueValidator(100)])
    file = models.FileField(upload_to='project_task')

    class Meta:
        ordering = ['project', 'name']

    def __str__(self):
        return(self.name)




class Issues(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="issues")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, blank=True, null=True, related_name="issues")
    status = models.CharField(max_length=7, choices=STATUS, default=1)
    due = models.CharField(max_length=7, choices=DUE, default=1)
    today_start_work = models.TimeField()
    today_end_work = models.TimeField()
    total_data_entry_today = models.CharField(max_length=254, default=0, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    complete_per = models.FloatField(max_length=4, blank=True, null=True, validators = [MinValueValidator(0), MaxValueValidator(100)])
    file = models.FileField(upload_to='task_issues')

    class Meta:
        verbose_name_plural = 'Issues'

    def __str__(self):
        return(self.project.name)
    


class ProjectSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'project_submissions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name= 'project_submissions')
    status = models.CharField(max_length=7, choices=STATUS, default=1)
    description = QuillField()
    file = models.FileField(upload_to='project_submission', max_length=254)
    

    def __str__(self):
        return f"task submission of => {self.project.name}"
    



    

# Hey,
# Arif Bhy In above I have added many choices that can assain as project pirity , risk and many more you can add this If you thinik this is good !
