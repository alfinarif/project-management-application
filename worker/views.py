from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from django.views.generic import TemplateView
from projects.forms import IssuesModelForm, ProjectSubmissionModelForm, TaskModelForm
from projects.models import Issues, Project, ProjectSubmission, Task
from django.db.models import Q
from django.contrib import messages
from payments.models import Payments
import datetime


class WorkerDashboardTemplateAPIView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                return redirect('leader:leader_dashboard')
            elif request.user.user_type == 'worker':
                if request.user.profile.is_fully_filled():
                    # project filtering object
                    worker_project_obj = Project.objects.filter(worker=request.user).first()
                    # project filtering object

                    # tasks and issues filtering
                    worker_task = Task.objects.filter(Q(worker=request.user) & Q(status='done'))
                    worker_issues = Issues.objects.filter(Q(project__worker=request.user))
                    # tasks and issues filtering

                    # project submited filtering object
                    project_submited_obj = ProjectSubmission.objects.filter(Q(project__worker=request.user, status='done') & Q(project__status='done'))
                    # project submited filtering object
                    # earning filtering here ===============
                    payment_worker_obj = Payments.objects.filter(receivers=request.user)
                    # earning filtering here ================
                    if payment_worker_obj.exists():
                        get_worker_earnings = payment_worker_obj.first()
                        context = {
                            'total_project_accept': worker_project_obj.project_accept(request.user),
                            'total_project_pending': worker_project_obj.project_pending(request.user),
                            'total_project_decline': worker_project_obj.project_decline(request.user),
                            'total_project_submited': project_submited_obj,
                            'worker_task': worker_task,
                            'worker_issues': worker_issues,
                            'totals_earning': get_worker_earnings.totals_earning(request.user),
                            'today_earning': get_worker_earnings.today_earning(request.user),
                            'week_earning': get_worker_earnings.week_earning(request.user),
                            'month_earning': get_worker_earnings.month_earning(request.user),
                            'year_earning': get_worker_earnings.year_earning(request.user)
                        }
                        messages.info(request, f"Hello '{request.user}' Welcome back to your dashboard..!")
                        return render(request, 'worker/index.html', context)
                    else:
                        context = {
                            'total_project_accept': 0,
                            'total_project_pending': 0,
                            'total_project_decline': 0,
                            'total_project_submited': 0,
                            'worker_task': worker_task,
                            'worker_issues': worker_issues,
                            'totals_earning': 0,
                            'today_earning': 0,
                            'week_earning': 0,
                            'month_earning': 0,
                            'year_earning': 0
                        }
                        messages.info(request, f"Hello '{request.user}' Welcome back to your dashboard..!")
                        return render(request, 'worker/index.html', context)
                else:
                    return redirect('accounts:accounts_edit_profile')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        pass

# project List view
class ProjectListTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.is_fully_filled():
                # redirect to user dashboard
                if request.user.user_type == 'admin':
                    return redirect('admin_dashboard:admin_dashboard')
                elif request.user.user_type == 'leader':
                    return redirect('leader:leader_dashboard')
                elif request.user.user_type == 'worker':
                    projects = Project.objects.filter(Q(worker = request.user) & Q(is_active = True)).order_by('-id')
                    context = {
                        'projects': projects
                    }
                    return render(request, 'worker/projects.html', context)
                else:
                    return redirect('accounts:login')
            else:
                return redirect('accounts:accounts_edit_profile')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        pass

# project detials view
class ProjectDetailTemplateView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.is_fully_filled():
                # redirect to user dashboard
                if request.user.user_type == 'admin':
                    return redirect('admin_dashboard:admin_dashboard')
                elif request.user.user_type == 'leader':
                    return redirect('leader:leader_dashboard')
                elif request.user.user_type == 'worker':
                    project = Project.objects.get(id=pk)
                    tasks = Task.objects.filter(project=project).order_by('-id')

                    form = ProjectSubmissionModelForm()
                    issues_form = IssuesModelForm()
                    
                    context = {
                        'project': project,
                        'tasks': tasks,
                        'form': form,
                        'issues_form': issues_form
                    }
                    return render(request, 'worker/project_detail.html', context)
                else:
                    return redirect('accounts:login')
            else:
                return redirect('accounts:accounts_edit_profile')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'post' or request.method == 'POST':
                # here will execude tasks
                project_id = request.POST.get('project_id')
                project_obj = Project.objects.get(id=project_id)
                postData = {
                    'project': project_obj,
                    'description': request.POST.get('description'),
                    'file': request.POST.get('file')
                }
                form = ProjectSubmissionModelForm(postData, request.FILES)
                # Issues form submission ======================================
                issues_form = IssuesModelForm(request.POST, request.FILES)

                # Project form submission ======================================
                if form.is_valid():
                    if ProjectSubmission.objects.filter(project=project_id).exists():
                        messages.info(request, "This Project Has Been Submited..!")
                        return redirect('worker:worker_project')
                    else:
                        instance = form.save(commit=False)
                        instance.user = request.user
                        instance.status = 'done'
                        instance.save()
                        ## here will update all {project, task} status to DONE becouse project is submited
                        project_obj.status = 'done'
                        project_obj.complete_per = 100
                        for task in project_obj.tasks.all():
                            task.status = 'done'
                            task.due = 'done'
                            task.save()
                        project_obj.save()
                        ## end updated all info
                        # update payments info
                        if Payments.objects.filter(receivers=request.user, project=project_obj).exists():
                            payment_obj = Payments.objects.filter(receivers=request.user, project=project_obj).first()
                            payment_obj.is_received = True
                            payment_obj.is_accept = True
                            payment_obj.save()
                        # update payments info

                        messages.info(request, "'Congratulations!' Project Successfully Submited..!")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                # Issues form submission ======================================
                if issues_form.is_valid():
                    instance = issues_form.save(commit=False)
                    instance.user = request.user
                    instance.project = project_obj
                    instance.task = None
                    instance.is_active = True
                    instance.save()
                    messages.info(request, "Issues Successfully..!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

        else:
            return redirect('accounts:login')

# project accept view
class AcceptProjectTemplateView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.is_fully_filled():
                # redirect to user dashboard
                if request.user.user_type == 'admin':
                    return redirect('admin_dashboard:admin_dashboard')
                elif request.user.user_type == 'leader':
                    return redirect('leader:leader_dashboard')
                elif request.user.user_type == 'worker':
                    project = Project.objects.get(id=pk)
                    project.status = 'stuck'
                    project.accept_status = 'accept'
                    project.save()
                    messages.info(request, "'Congratulations!' You have accept new project..!")
                    return redirect('worker:worker_project')
                else:
                    return redirect('accounts:login')
            else:
                return redirect('accounts:accounts_edit_profile')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        pass

# Task list and create view
class TaskListTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.is_fully_filled():
                # redirect to user dashboard
                if request.user.user_type == 'admin':
                    return redirect('admin_dashboard:admin_dashboard')
                elif request.user.user_type == 'leader':
                    return redirect('leader:leader_dashboard')
                elif request.user.user_type == 'worker':
                    tasks = Task.objects.filter(Q(project__worker=request.user) & Q(is_active=True)).order_by('-id')
                    task_issues = Issues.objects.filter(Q(project__worker=request.user) & Q(is_active=True)).order_by('-id')
                    
                    context = {
                        'tasks': tasks,
                        'task_issues': task_issues
                    }
                    return render(request, 'worker/tasks.html', context)
                else:
                    return redirect('accounts:login')
            else:
                return redirect('accounts:accounts_edit_profile')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'post' or request.method == 'POST':
                # here will execude tasks
                pass
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

        else:
            return redirect('accounts:login')

# Project Submission view
class SubmitedProjectsTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.is_fully_filled():
                # redirect to user dashboard
                if request.user.user_type == 'admin':
                    return redirect('admin_dashboard:admin_dashboard')
                elif request.user.user_type == 'leader':
                    return redirect('leader:leader_dashboard')
                elif request.user.user_type == 'worker':
                    submited_projects = ProjectSubmission.objects.filter(Q(project__worker=request.user) & Q(project__status='done')).order_by('-id')
                    context = {
                        'submited_projects': submited_projects
                    }
                    return render(request, 'worker/project_submission.html', context)
                else:
                    return redirect('accounts:login')
            else:
                return redirect('accounts:accounts_edit_profile')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'post' or request.method == 'POST':
                # here will execude tasks
                pass
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

        else:
            return redirect('accounts:login')

# My Payments view
class MyPaymentsTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.is_fully_filled():
                # redirect to user dashboard
                if request.user.user_type == 'admin':
                    return redirect('admin_dashboard:admin_dashboard')
                elif request.user.user_type == 'leader':
                    return redirect('leader:leader_dashboard')
                elif request.user.user_type == 'worker':
                    my_payments = Payments.objects.filter(Q(receivers=request.user) & Q(project__worker=request.user) & Q(project__status='done', is_received=True)).order_by('-id')
                    context = {
                        'my_payments': my_payments
                    }
                    return render(request, 'worker/my_payments.html', context)
                else:
                    return redirect('accounts:login')
            else:
                return redirect('accounts:accounts_edit_profile')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'post' or request.method == 'POST':
                # here will execude tasks
                pass
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

        else:
            return redirect('accounts:login')
