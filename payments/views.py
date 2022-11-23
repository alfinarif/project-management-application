from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from accounts.models import User, Notification
from payments.forms import PaymentsProjectForm, PaymentWorkerForm
from payments.models import Payments
from projects.models import Project
import datetime
from django.contrib import messages


# payment worker creation view
class PaymentProjectBasedTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # redirect to user dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                # project_id = request.GET.get('pay_for')
                # project_obj = Project.objects.get(id=project_id)
                # workers = project_obj.worker.all()

                form = PaymentsProjectForm()
                context = {
                    'form': form
                }
                return render(request, 'payments/payment_project_based.html', context)
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'post' or request.method == 'POST':
                # here will execute tasks
                project_id = request.GET.get('pay_for')
                project_obj = Project.objects.get(id=project_id)
                form = PaymentsProjectForm(request.POST, request.FILES)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.project = project_obj
                    instance.sender = request.user
                    instance.date = datetime.date.today()
                    instance.save()
                    for worker in request.POST.getlist('receivers'):
                        instance.receivers.add(worker)
                    messages.success(request, "Payment has been sended!")
                    notification_obj = Notification.objects.create(from_leader=request.user, subject="Payments Info", is_active=True, message="Congratulation! you have a new payments let confirm it.")
                    for to_worker in request.POST.getlist('receivers'):
                        notification_obj.to_worker.add(to_worker)
                        notification_obj.save()
                    return redirect('leader:leader_project')
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

        else:
            return redirect('accounts:login')



# payment worker creation view
class PaymentWorkerTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # redirect to user dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                form = PaymentWorkerForm()
                context = {
                    'form': form
                }
                return render(request, 'payments/payment_worker.html', context)
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'post' or request.method == 'POST':
                # here will execute tasks
                form = PaymentWorkerForm(request.POST, request.FILES)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.sender = request.user
                    instance.is_received = True
                    instance.is_accept = True
                    instance.date = datetime.date.today()
                    instance.save()
                    for worker in request.POST.getlist('receivers'):
                        instance.receivers.add(worker)
                    messages.success(request, "Payment submited successfully..!")
                    notification_obj = Notification.objects.create(from_leader=request.user, subject="Payments Info", is_active=True, message="Congratulation! you have a new payments let confirm it.")
                    for to_worker in request.POST.getlist('receivers'):
                        notification_obj.to_worker.add(to_worker)
                        notification_obj.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.warning(request, "Failed payment request try again..!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

        else:
            return redirect('accounts:login')

