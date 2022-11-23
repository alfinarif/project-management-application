from django.urls import path
from payments import views

app_name = "payments"
urlpatterns = [
    path('worker/', views.PaymentProjectBasedTemplateView.as_view(), name='payment_project_based'),
    path('send/worker/', views.PaymentWorkerTemplateView.as_view(), name='payment_worker'),
]
