from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.db import models
import uuid

class Ticket(models.Model):
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    CLOSED = 'CLOSED'

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (IN_PROGRESS, 'In Progress'),
        (CLOSED, 'Closed'),
    ]
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=OPEN)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    assigned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_tickets", blank=True)

    def __str__(self):
        return self.title


class TicketAssignment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="assignments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ticket_assignments")
    assigned_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.email} assigned to {self.ticket.title}"


class TicketActivity(models.Model):
    ACTIVITY_TYPES = [
        ('comment', 'Comment'),
        ('status_change', 'Status Change'),
        ('note', 'Note'),
    ]
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="activities")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated this line
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Activity by {self.user} on {self.ticket.title} ({self.activity_type})"
