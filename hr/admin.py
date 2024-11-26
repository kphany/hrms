# hr/admin.py

from django.contrib import admin
from .models import (
    Employee,
    Attendance,
    Leave,
    Appraisal,
    Announcement,
    Resignation,
    Department,
    CompanyProfile,
    Settings,
)

# Custom admin for Company
@admin.register(CompanyProfile)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country', 'established_date')
    search_fields = ('name', 'city', 'state')

# Custom admin for Employee
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'staff_id', 'department', 'date_joined')
    search_fields = ('first_name', 'last_name', 'staff_id', 'email')

# Custom admin for Leave
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'status')
    list_filter = ('status',)

# Custom admin for Appraisal
@admin.register(Appraisal)
class AppraisalAdmin(admin.ModelAdmin):
    list_display = ('employee', 'score', 'review_date')
    search_fields = ('employee__user__username',)  # Enables searching by username
    list_filter = ('review_date',)  # Enables filtering by review date

# Register models with custom admin
admin.site.register(Employee, EmployeeAdmin)  # Keep this registration
admin.site.register(Attendance)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(Announcement)
admin.site.register(Resignation)
admin.site.register(Department)

# Custom admin for Settings
@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('setting1', 'setting2', 'created_at', 'updated_at')
