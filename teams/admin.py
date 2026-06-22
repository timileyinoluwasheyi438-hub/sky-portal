from django.contrib import admin
from .models import Department, Team, Engineer, Dependency, AuditLog

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'manager', 'status']
    list_filter = ['status', 'department']
    search_fields = ['name']

@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'team']

@admin.register(Dependency)
class DependencyAdmin(admin.ModelAdmin):
    list_display = ['team', 'depends_on']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action']
    readonly_fields = ['timestamp', 'user', 'action', 'details']