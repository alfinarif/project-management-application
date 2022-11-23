from django.db import models
from accounts.models import User
from projects.models import Project
from django.db.models import Q
import datetime

# Payment model
class Payments(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments', blank=False, null=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leader_payments', blank=False, null=False)
    receivers = models.ManyToManyField(User, related_name='worker_payments', blank=False)
    amount = models.FloatField(default=0, blank=False, null=False)
    per_entry = models.FloatField(default=0, blank=True, null=True)
    salary = models.FloatField(default=0, blank=True, null=True)
    is_received = models.BooleanField(default=False)
    is_accept = models.BooleanField(default=False)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Payment to {self.project}"
    
    class Meta:
        verbose_name_plural = 'Payments Employee'

    def entry_totals(self):
        totals = 0
        for entry in self.project.issues.all():
            totals += int(entry.total_data_entry_today)
        return totals*self.per_entry

    def total_entry_amount(self, user):
        total_per_entry = 0
        total_entry = 0
        payment_obj = Payments.objects.filter(Q(receivers=user) & Q(project__worker=user) & Q(project__status='done', is_received=True))
        for project in payment_obj:
            total_per_entry += project.per_entry
            for issues in project.project.issues.all():
                if int(issues.total_data_entry_today) == 0:
                    pass
                else:
                    total_entry += int(issues.total_data_entry_today)
            
        return total_entry*total_per_entry
    
    # today earning
    def today_earning(self, user):
        # today earning
        today = datetime.date.today()
        today_earning_obj = Payments.objects.filter(Q(date=today) & Q(receivers=user) & Q(project__worker=user) & Q(project__status='done', is_received=True))
        today_earning = 0
        if today_earning_obj.exists():
            for today_earn in today_earning_obj:
                today_earning += today_earn.amount
            return today_earning + self.total_entry_amount(user)
        else:
            return today_earning

    # this week earning
    def week_earning(self, user):
        # this week earning
        week_start = datetime.date.today()
        week_start -= datetime.timedelta(days=week_start.weekday())
        week_end = week_start + datetime.timedelta(days=7)
        this_week_earning_obj = Payments.objects.filter(Q(date__gte=week_start, date__lt=week_end) & Q(receivers=user) & Q(project__worker=user) & Q(project__status='done', is_received=True, is_accept=True))
        if this_week_earning_obj.exists():
            week_earning = 0
            for week_earn in this_week_earning_obj:
                week_earning += week_earn.amount
            return week_earning + self.total_entry_amount(user)
        else:
            return 0

    # this month earning
    def month_earning(self, user):
        # this month earning
        this_month_earning_obj = Payments.objects.filter(Q(date__gte=datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)) & Q(receivers=user) & Q(project__worker=user) & Q(project__status='done', is_received=True, is_accept=True))
        if this_month_earning_obj.exists():
            month_earning = 0
            for month_earn in this_month_earning_obj:
                month_earning += month_earn.amount
            return month_earning + self.total_entry_amount(user)
        else:
            return 0

    # this year earning
    def year_earning(self, user):
        # this year earning
        this_year_earning_obj = Payments.objects.filter(Q(date__year=datetime.datetime.now().year) & Q(receivers=user) & Q(project__worker=user) & Q(project__status='done', is_received=True, is_accept=True))
        if this_year_earning_obj.exists():
            year_earning = 0
            for year_earn in this_year_earning_obj:
                year_earning += year_earn.amount
            return year_earning + self.total_entry_amount(user)
        else:
            return 0
    
    # current user totals earnings
    def totals_earning(self, user):
        totals_earning_obj = Payments.objects.filter(Q(project__status='done') & Q(receivers=user) & Q(project__worker=user) & Q(is_received=True, is_accept=True))
        if totals_earning_obj.exists():
            totals_earning = 0
            for worker in totals_earning_obj:
                totals_earning += worker.amount
            return totals_earning + self.total_entry_amount(user)
        else:
            return 0