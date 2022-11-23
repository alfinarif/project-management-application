from django.urls import path
from leader import views

app_name = 'leader'
urlpatterns = [
    path('dashboard/', views.LeaderDashboardAPIView.as_view(), name='leader_dashboard'),
    path('dashboard/worker/', views.WorkerListTemplateAPIView.as_view(), name='leader_worker'),
    path('dashboard/project/', views.ProjectListTemplateAPIView.as_view(), name='leader_project'),
    path('dashboard/project/<str:pk>/', views.ProjectDetailTemplateAPIView.as_view(), name='leader_project_detail'),
    path('dashboard/project/add/new/', views.ProjectCreateTemplateAPIView.as_view(), name='leader_project_add'),
    path('dashboard/project/submited/list/', views.SubmitedProjectsTemplateAPIView.as_view(), name='leader_project_submission'),
    path('dashboard/task/', views.TaskListTemplateAPIView.as_view(), name='leader_task'),
    path('dashboard/notification/send/', views.SendNotificationTemplateView.as_view(), name='leader_send_notification'),
]
