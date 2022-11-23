from django import forms
from django.contrib.auth import get_user_model
from projects.models import Project
from payments.models import Payments
User = get_user_model()

# pay project based form
class PaymentsProjectForm(forms.ModelForm):
    receivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(user_type='worker'),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Payments
        fields = [
            'amount',
            'per_entry',
            'receivers',
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}), 
            'per_entry': forms.NumberInput(attrs={'class': 'form-control'}), 
        }


# pay to direct worker form
class PaymentWorkerForm(forms.ModelForm):
    receivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(user_type='worker'),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Payments
        fields = [
            'project',
            'amount',
            'per_entry',
            'receivers',
        ]
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}), 
            'amount': forms.NumberInput(attrs={'class': 'form-control'}), 
            'per_entry': forms.NumberInput(attrs={'class': 'form-control'}), 
        }
