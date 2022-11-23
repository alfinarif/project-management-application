from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('register/leader/', views.LeaderRegisterTemplateView.as_view(), name='register_leader'), # leader register route
    path('register/worker/', views.WorkerRegisterTemplateView.as_view(), name='register_worker'), # worker register route
    path('', views.LoginTemplateView.as_view(), name='login'), # login page route
    path('accounts/logout/', views.logoutView, name='logout'), # logout page route
    path('worker/dashboard/profile/', views.ProfileTemplateView.as_view(), name='accounts_profile'), # login page route
    path('worker/dashboard/profile/edit/', views.EditProfileTemplateView.as_view(), name='accounts_edit_profile'), # login page route
    path('worker/dashboard/notification/seen/<str:pk>/', views.seenNotification, name='accounts_seen_notification'),
]
