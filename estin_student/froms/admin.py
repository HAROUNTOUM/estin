from django.contrib import admin
from .models import Module, Resource


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display  = ['name', 'level', 'semester']
    list_filter   = ['level', 'semester']
    search_fields = ['name']
    ordering      = ['level', 'semester', 'name']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display  = ['title', 'module', 'resource_type', 'academic_year', 'uploaded_by', 'downloads', 'is_verified', 'uploaded_at']
    list_filter   = ['resource_type', 'is_verified', 'module__level', 'module__semester']
    search_fields = ['title', 'module__name']
    readonly_fields = ['file_hash', 'drive_id', 'downloads', 'uploaded_at']
    actions       = ['mark_verified']

    @admin.action(description='Mark selected resources as verified')
    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)
