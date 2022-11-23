from django.urls import path
from admin_dashboard import views

app_name = 'admin_dashboard'
urlpatterns = [
    path('dashboard/', views.AdminDashboardTemplateAPIView.as_view(), name='admin_dashboard'),
]
