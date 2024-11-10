from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings 
from django.apps import apps # To reference the custom user model
from .models import Ticket, TicketActivity, TicketAssignment
from .forms import TicketForm, TicketActivityForm,TicketStatusForm
from django.contrib import messages
# Get the custom user model class dynamically
User = apps.get_model(settings.AUTH_USER_MODEL)

# Check if the user is a superuser
def is_superuser(user):
    return user.is_superuser

# List all tickets
@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

# Create a new ticket
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creator = request.user  # Assign the logged-in user as the creator
            ticket.save()
            messages.success(request, 'Ticket created successfully!')
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})

# View ticket details
@login_required
def ticket_detail(request, ticket_uuid):
    ticket = get_object_or_404(Ticket, uuid=ticket_uuid)
    # Check if the user is assigned to the ticket or if they are a superuser
    if not (request.user.is_superuser or request.user == ticket.creator or request.user in ticket.assigned_users.all()):
            messages.error(request, "You don't have permission to access this ticket.")
            return redirect('ticket_list')  # Redirect to the ticket list
    if request.method == 'POST':
        # Handle ticket status update (if the form for status update is submitted)
        if 'update_status' in request.POST:
            status_form = TicketStatusForm(request.POST, instance=ticket)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Ticket status updated successfully!')
                return redirect('ticket_detail', ticket_uuid=ticket.uuid)
        
        # Handle the activity form submission (e.g., status change, comments, etc.)
        activity_form = TicketActivityForm(request.POST)
        if activity_form.is_valid():
            activity = activity_form.save(commit=False)
            activity.ticket = ticket
            activity.user = request.user
            activity.save()
            messages.success(request, 'Activity added successfully!')
            return redirect('ticket_detail', ticket_uuid=ticket.uuid)
    else:
        # If not a POST request, initialize forms
        status_form = TicketStatusForm(instance=ticket)
        activity_form = TicketActivityForm()

    # Fetch ticket activities
    activities = TicketActivity.objects.filter(ticket=ticket).order_by('-created_at')

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'status_form': status_form,
        'activity_form': activity_form,
        'activities': activities,
    })

# Assign users to a ticket
@login_required
@user_passes_test(is_superuser)  # Restrict access to superusers only
def assign_ticket(request, ticket_uuid):
    ticket = get_object_or_404(Ticket, uuid=ticket_uuid)
    print(ticket)
    if request.method == 'POST':
        user_ids = request.POST.getlist('users')
        users = User.objects.filter(uuid__in=user_ids)  # Fetch users by IDs from the form
        ticket.assigned_users.set(users)  # Assign users to the ticket
        ticket.save()  # Save the changes to the ticket
        for user in users:
            TicketAssignment.objects.create(ticket=ticket, user=user)
        messages.success(request, 'Users assigned to ticket successfully!')
        return redirect('ticket_detail', ticket_uuid=ticket.uuid)
    else:
        # Use the custom user model to fetch all users
        users = User.objects.all()
    return render(request, 'tickets/assign_ticket.html', {'ticket': ticket, 'users': users})


# Add activity to ticket (status change, comments, etc.)
@login_required
def add_activity(request, ticket_uuid):
    ticket = get_object_or_404(Ticket, uuid=ticket_uuid)
    if request.method == 'POST':
        form = TicketActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.ticket = ticket
            activity.user = request.user
            activity.save()
            messages.success(request, 'Activity added successfully!')
            return redirect('ticket_detail', ticket_uuid=ticket.uuid)
    else:
        form = TicketActivityForm()
    return render(request, 'tickets/add_activity.html', {'form': form, 'ticket': ticket})


# Delete ticket (only superusers can delete tickets)
@login_required
@user_passes_test(is_superuser)
def delete_ticket(request, ticket_uuid):
    ticket = get_object_or_404(Ticket, uuid=ticket_uuid)
    ticket.delete()
    messages.success(request, 'Ticket deleted successfully!')
    return redirect('ticket_list')