from django import forms
from .models import Ticket,TicketActivity
from django.contrib.auth import get_user_model

class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']

class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']
        
        # You can add custom labels or help texts if necessary
        labels = {
            'title': 'Ticket Title',
            'description': 'Ticket Description',
            'priority': 'Ticket Priority',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the issue...'}),
        }        

class TicketActivityForm(forms.ModelForm):
    class Meta:
        model = TicketActivity
        fields = ['activity_type', 'description']
        
        # Optionally customize labels if necessary
        labels = {
            'activity_type': 'Activity Type',
            'description': 'Activity Description',
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter activity details...'}),
        }

class TicketAssignForm(forms.ModelForm):
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),  # Get all users
        widget=forms.CheckboxSelectMultiple,
        required=False  # Make this field optional (if no user is assigned, it's fine)
    )

    class Meta:
        model = Ticket
        fields = ['assigned_users']