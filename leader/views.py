from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from projects.models import Categories, Project, Task, Issues, ProjectSubmission
from projects.forms import ProjectModelForm, TaskModelForm, ProjectSubmissionModelForm, IssuesModelForm
from accounts.forms import RegisterForm, NotificationForm

User = get_user_model()

# leader dashboard index view
class LeaderDashboardAPIView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # admin access
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')

            # leader access
            elif request.user.user_type == 'leader':
                if request.user.profile.is_fully_filled():
                    # count area
                    worker_count = User.objects.filter(user_type = 'worker').count()
                    projects_count = Project.objects.filter(Q(leader=request.user) & Q(is_active = True)).count()
                    tasks_count = Task.objects.filter(is_active = True).count()
                    submission_task_count = '0'

                    # object filter area
                    ongoing_projects = Project.objects.filter(Q(leader=request.user) & Q(is_active = True)).order_by('-id')

                    context = {
                        'worker_count': worker_count,
                        'projects_count': projects_count,
                        'tasks_count': tasks_count,
                        'submission_task_count': submission_task_count,
                        'ongoing_projects': ongoing_projects
                    }
                    return render(request, 'leader/index.html', context)
                else:
                    return redirect('accounts:accounts_edit_profile')
            
            # worker access
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        pass

# worker creation and list view
class WorkerListTemplateAPIView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # admin access
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')

            # leader access
            elif request.user.user_type == 'leader':
                workers = User.objects.filter(user_type='worker').order_by('-id')
                context = {
                    'workers': workers
                }
                return render(request, 'leader/workers.html', context)
            
            # worker access
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # admin access
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            # leader access
            elif request.user.user_type == 'leader':
                email = request.POST.get('email')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                formData = {
                    'email': email,
                    'password1': password1,
                    'password2': password2
                }
                form = RegisterForm(formData)
                
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.user_type = 'worker'
                    instance.is_active = True
                    instance.save()
                    return redirect('leader:leader_worker')
                
                context = {
                    
                }
                return render(request, 'leader/new_worker.html', context)
            # worker access
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        
        else:
            return redirect('accounts:login')

# project List view
class ProjectListTemplateAPIView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # redirect to user dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                projects = Project.objects.filter(Q(leader=request.user) & Q(is_active = True)).order_by('-id')
                context = {
                    'projects': projects
                }
                return render(request, 'leader/projects.html', context)
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        pass

# project detials view
class ProjectDetailTemplateAPIView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            # redirect to user dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
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
                return render(request, 'leader/project_detail.html', context)
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
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
                        return redirect('leader:leader_project')
                    else:
                        instance = form.save(commit=False)
                        instance.user = request.user
                        instance.status = 'done'
                        ## here will update all {project, task} status to DONE becouse project is submited
                        project_obj.status = 'done'
                        project_obj.complete_per = 100
                        for task in project_obj.tasks.all():
                            task.status = 'done'
                            task.due = 'done'
                            task.save()
                        project_obj.save()
                        ## end updated all info
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                # Issues form submission ======================================
                if issues_form.is_valid():
                    instance = issues_form.save(commit=False)
                    instance.project = project_obj
                    instance.task = None
                    instance.is_active = True
                    instance.save()
                    return redirect('leader:leader_project')
                
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
                
            
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

        else:
            return redirect('accounts:login')

# project creation view
class ProjectCreateTemplateAPIView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # redirect to user dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                form = ProjectModelForm()
                context = {
                    'form': form
                }
                return render(request, 'leader/new_project.html', context)
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'post' or request.method == 'POST':
                # here will execude tasks
                form = ProjectModelForm(request.POST, request.FILES)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.leader = request.user
                    instance.complete_per = 0
                    instance.is_active = True
                    instance.accept_status = 'draft'
                    instance.save()
                    for worker in request.POST.getlist('worker'):
                        instance.worker.add(worker)

                    return redirect(reverse('payments:payment_project_based') + "?pay_for=" + str(instance.pk))
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

        else:
            return redirect('accounts:login')

# Task creation and list view
class TaskListTemplateAPIView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # redirect to user dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                tasks = Task.objects.filter(Q(project__leader=request.user) & Q(is_active=True)).order_by('-id')
                task_issues = Issues.objects.filter(Q(project__leader=request.user) & Q(is_active=True)).order_by('-id')
                
                task_form = TaskModelForm()
                context = {
                    'tasks': tasks,
                    'task_issues': task_issues,
                    'task_form': task_form
                }
                return render(request, 'leader/tasks.html', context)
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'post' or request.method == 'POST':
                # here will execude tasks
                form = TaskModelForm(request.POST, request.FILES)
                if form.is_valid():
                    instance = form.save()
                    print('=================================')
                    print(instance)
                    print('=================================')
                    for worker in request.POST.getlist('worker'):
                        instance.worker.add(worker)
                    return redirect('leader:leader_task')
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

        else:
            return redirect('accounts:login')

# Project Submission view
class SubmitedProjectsTemplateAPIView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # redirect to user dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                submited_projects = ProjectSubmission.objects.filter(project__leader=request.user, project__status='done').order_by('-id')
                context = {
                    'submited_projects': submited_projects
                }
                return render(request, 'leader/project_submission.html', context)
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
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

# Send Notification view
class SendNotificationTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.is_fully_filled():
                # redirect to user dashboard
                if request.user.user_type == 'admin':
                    return redirect('admin_dashboard:admin_dashboard')
                elif request.user.user_type == 'leader':
                    notification_form = NotificationForm()
                    context = {
                        'notification_form': notification_form
                    }
                    return render(request, 'leader/send_notification.html', context)
                elif request.user.user_type == 'worker':
                    return redirect('worker:worker_dashboard')
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
                notification_form = NotificationForm(request.POST, request.FILES)
                if notification_form.is_valid():
                    instance = notification_form.save(commit=False)
                    instance.from_leader = request.user
                    instance.save()
                    for worker in request.POST.getlist('to_worker'):
                        instance.to_worker.add(worker)
                    return redirect('leader:leader_dashboard')
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

        else:
            return redirect('accounts:login')



