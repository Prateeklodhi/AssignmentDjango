from django.contrib import admin
from .models import Ticket, TicketActivity, TicketAssignment

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'creator')
    search_fields = ('title', 'description')

@admin.register(TicketActivity)
class TicketActivityAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'activity_type', 'created_at')
    list_filter = ('activity_type', 'created_at')

@admin.register(TicketAssignment)
class TicketAssignmentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user')
