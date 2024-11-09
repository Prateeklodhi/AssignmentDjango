from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),  # List of all tickets
    path('create/', views.create_ticket, name='create_ticket'),  # Create a new ticket
    path('<uuid:ticket_uuid>/', views.ticket_detail, name='ticket_detail'),  # View ticket details
    path('<uuid:ticket_uuid>/assign/', views.assign_ticket, name='assign_ticket'),  # Assign users to ticket
    path('<uuid:ticket_uuid>/add_activity/', views.add_activity, name='add_activity'),  # Add activity to ticket
]
