from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render

from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.forms import RegisterForm, ProfileForm

from django.contrib.auth import logout

from django.contrib.auth import authenticate, login, logout
from accounts.models import Notification, Profile
User = get_user_model() # get user models

# Leader user registration view 
class LeaderRegisterTemplateView(TemplateView):
    # get method to view the page
    def get(self, request, *args, **kwargs):
        # check user authenticated
        if request.user.is_authenticated:
            # redirect to user dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                return redirect('leader:leader_dashboard')
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        else:

            # send context to template 
            context = {
                
            }
            # render template
            return render(request, 'accounts/register.html', context) # render a template with context

    # post method to handle user submited data and create user object
    def post(self, request, *args, **kwargs):
        # check if user is authenticate == True or False
        if request.user.is_authenticated:
            # if user is authenticated then user will be redirect to dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                return redirect('leader:leader_dashboard')
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        else:
            # check again is it post method or not, (to more secure)
            if request.method == 'post' or request.method == 'POST':
                postData = {
                    'email': request.POST.get('email'),
                    'password1': request.POST.get('password1'),
                    'password2': request.POST.get('password2')
                }
                form = RegisterForm(postData) # pass user submited data to RegisterForm 
                if form.is_valid(): # check the submited data is valid
                    try: # inside try we gonna check user is exist == True or False
                        email = form.cleaned_data['email'] # get submited user email
                        if User.objects.get(email=email).count() > 0: # check user submited email is exist == True or False
                            messages.warning(request, "This email address already exist!") # send message to user
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon
                        else:
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon
                    except: # here we gonna create user object
                        instance = form.save(commit=False)# commit false given access to reasign value
                        instance.user_type = 'leader' # reaign the value
                        instance.is_active = True # now direct active user account (when verify user we gonna change it)
                        instance.save() # save those data to database
                        return redirect('accounts:login') # redirect to login page after created account
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon


# Worker user registration view 
class WorkerRegisterTemplateView(TemplateView):
    # get method to view the page
    def get(self, request, *args, **kwargs):
        # check user authenticated
        if request.user.is_authenticated:
            # redirect to user dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                return redirect('leader:leader_dashboard')
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        else:
            # send context to template 
            context = {

            }
            # render template
            return render(request, 'accounts/register.html', context) # render a template with context

    # post method to handle user submited data and create user object
    def post(self, request, *args, **kwargs):
        # check if user is authenticate == True or False
        if request.user.is_authenticated:
            # if user is authenticated then user will be redirect to dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                return redirect('leader:leader_dashboard')
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        else:
            # check again is it post method or not, (to more secure)
            if request.method == 'post' or request.method == 'POST':
                postData = {
                    'email': request.POST.get('email'),
                    'password1': request.POST.get('password1'),
                    'password2': request.POST.get('password2')
                }
                form = RegisterForm(postData) # pass user submited data to RegisterForm 
                if form.is_valid(): # check the submited data is valid
                    try: # inside try we gonna check user is exist == True or False
                        email = form.cleaned_data['email'] # get submited user email
                        if User.objects.get(email=email).count() > 0: # check user submited email is exist == True or False
                            messages.warning(request, "This email address already exist!") # send message to user
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon
                        else:
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon
                    except: # here we gonna create user object
                        instance = form.save(commit=False) # commit false given access to reasign value
                        instance.user_type = 'worker'# reaign the value
                        instance.is_active = True # now direct active user account (when verify user we gonna change it)
                        instance.save()# save those data to database
                        return redirect('accounts:login') # redirect to login page after created account
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

  
# user login template view
class LoginTemplateView(TemplateView):
    # get method to render templates
    def get(self, request, *args, **kwargs):
        # check user authentication
        if request.user.is_authenticated:
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                return redirect('leader:leader_dashboard')
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
            return HttpResponse('Redirect to dashboad coz user is authenticated')
        else:
            context = {
                
            }
            return render(request, 'accounts/login.html', context)
    # post method to login users
    def post(self, request, *args, **kwargs):
        # check user authentication
        if request.user.is_authenticated:
            # redirect to user dashboard
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                return redirect('leader:leader_dashboard')
            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
            else:
                return redirect('accounts:login')
        else:
            # check request method
            if request.method == 'post' or request.method == 'POST':
                email = request.POST.get('email') # get submited email
                password = request.POST.get('password') # get submited password
                user = authenticate(request, username=email, password=password) # authentication a user
                # check user is not none == True or False
                if user is not None:
                    login(request, user) # now login user
                    # given access by user type
                    if request.user.user_type == 'admin':
                        return redirect('admin_dashboard:admin_dashboard')
                    elif request.user.user_type == 'leader':
                        return redirect('leader:leader_dashboard')
                    elif request.user.user_type == 'worker':
                        return redirect('worker:worker_dashboard')
                    else:
                        return redirect('accounts:login')
                else:
                    # send a message to user
                    messages.info(request, "username or password is incorrect!")
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # return the same page if run this (else) conditon

# user logout view    
def logoutView(request):
    logout(request)
    return redirect('accounts:login')

# profile view
class ProfileTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                return redirect('leader:leader_dashboard')
            elif request.user.user_type == 'worker':
                
                context = {
                    
                }
                return render(request, 'accounts/profile.html', context)
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        pass


# edit profile
class EditProfileTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 'admin':
                return redirect('admin_dashboard:admin_dashboard')
            elif request.user.user_type == 'leader':
                return redirect('leader:leader_dashboard')
            elif request.user.user_type == 'worker':
                profile_obj = Profile.objects.get(user=request.user)
                worker_profile_form = ProfileForm(instance=profile_obj)
                context = {
                    'worker_profile_form': worker_profile_form
                }
                return render(request, 'accounts/edit_profile.html', context)
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'post' or request.method == 'POST':
                # save user info
                profile_obj = Profile.objects.get(user=request.user)
                worker_profile_form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
                if worker_profile_form.is_valid():
                    
                    worker_profile_form.save()
                    return redirect('accounts:accounts_profile')
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect('accounts:login')
        else:
            return redirect('accounts:login')

# Seen notification view
def seenNotification(request, pk):
    notification_obj = Notification.objects.get(id=pk)
    notification_obj.is_active = False
    notification_obj.is_seen = True
    notification_obj.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

