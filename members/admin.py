"""
Django Admin Configuration for Double C Ranch Portal
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Member, Document, SignedDocument,
    CheckIn, GoalRequest, Goal, GoalUpdate,
    Note, AuditLog
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'email_verified_at')}),
    )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Member Admin"""
    list_display = ('full_name', 'membership_tier', 'status', 'attendance_all_time', 'last_checkin_at', 'created_at')
    list_filter = ('status', 'membership_tier', 'certification_level')
    search_fields = ('first_name', 'last_name', 'parent_name', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at', 'attendance_30d', 'attendance_all_time', 'last_checkin_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'first_name', 'last_name', 'parent_name', 'phone')
        }),
        ('Membership', {
            'fields': ('membership_tier', 'status', 'certification_level')
        }),
        ('Statistics', {
            'fields': ('attendance_30d', 'attendance_all_time', 'last_checkin_at'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('id', 'created_at', 'updated_at', 'merged_into'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_members', 'disable_members']
    
    def approve_members(self, request, queryset):
        updated = queryset.update(status='Approved')
        self.message_user(request, f'{updated} members approved.')
    approve_members.short_description = "Approve selected members"
    
    def disable_members(self, request, queryset):
        updated = queryset.update(status='Disabled')
        self.message_user(request, f'{updated} members disabled.')
    disable_members.short_description = "Disable selected members"


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Document Template Admin"""
    list_display = ('name', 'code', 'version', 'is_active', 'is_required', 'created_at')
    list_filter = ('is_active', 'is_required')
    search_fields = ('name', 'code')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Document Info', {
            'fields': ('code', 'name', 'version', 'is_active', 'is_required')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('System', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SignedDocument)
class SignedDocumentAdmin(admin.ModelAdmin):
    """Signed Document Admin"""
    list_display = ('member', 'document', 'signed_name', 'signed_at', 'ip_address')
    list_filter = ('signed_at', 'document')
    search_fields = ('member__first_name', 'member__last_name', 'signed_name', 'signed_for_name')
    readonly_fields = ('id', 'signed_at', 'created_at', 'document_snapshot', 'ip_address', 'user_agent')
    
    fieldsets = (
        ('Signature Details', {
            'fields': ('document', 'member', 'user', 'signed_name', 'signed_for_name', 'relationship')
        }),
        ('Audit Trail', {
            'fields': ('signed_at', 'ip_address', 'user_agent')
        }),
        ('Legal Record', {
            'fields': ('document_snapshot',),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    """Check-In Admin"""
    list_display = ('member', 'type', 'status', 'requested_at', 'confirmed_at', 'instructor')
    list_filter = ('status', 'type', 'requested_at')
    search_fields = ('member__first_name', 'member__last_name', 'student_note', 'staff_note')
    readonly_fields = ('id', 'created_at', 'updated_at', 'requested_at')
    
    fieldsets = (
        ('Check-In Details', {
            'fields': ('member', 'type', 'status', 'requested_at', 'confirmed_at')
        }),
        ('Notes', {
            'fields': ('student_note', 'staff_note')
        }),
        ('Assignment & Approval', {
            'fields': ('instructor', 'created_by', 'approved_by')
        }),
        ('System', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_checkins', 'reject_checkins']
    
    def approve_checkins(self, request, queryset):
        for checkin in queryset.filter(status='Pending'):
            checkin.approve(request.user)
        self.message_user(request, f'{queryset.count()} check-ins approved.')
    approve_checkins.short_description = "Approve selected check-ins"
    
    def reject_checkins(self, request, queryset):
        updated = queryset.update(status='Rejected')
        self.message_user(request, f'{updated} check-ins rejected.')
    reject_checkins.short_description = "Reject selected check-ins"


@admin.register(GoalRequest)
class GoalRequestAdmin(admin.ModelAdmin):
    """Goal Request Admin"""
    list_display = ('member', 'timeframe', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('member__first_name', 'member__last_name', 'content')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Request Details', {
            'fields': ('member', 'submitted_by', 'content', 'timeframe', 'status')
        }),
        ('System', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    """Goal Admin"""
    list_display = ('member', 'title', 'status', 'target_date', 'created_by', 'created_at')
    list_filter = ('status', 'target_date', 'created_at')
    search_fields = ('member__first_name', 'member__last_name', 'title', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Goal Details', {
            'fields': ('member', 'created_by', 'title', 'description', 'target_date', 'status')
        }),
        ('System', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GoalUpdate)
class GoalUpdateAdmin(admin.ModelAdmin):
    """Goal Update Admin"""
    list_display = ('goal', 'author', 'author_type', 'created_at')
    list_filter = ('author_type', 'created_at')
    search_fields = ('goal__title', 'note')
    readonly_fields = ('id', 'created_at')
    
    fieldsets = (
        ('Update Details', {
            'fields': ('goal', 'author', 'author_type', 'note')
        }),
        ('System', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Note Admin"""
    list_display = ('member', 'category', 'visibility', 'author', 'created_at')
    list_filter = ('category', 'visibility', 'created_at')
    search_fields = ('member__first_name', 'member__last_name', 'content')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Note Details', {
            'fields': ('member', 'author', 'category', 'visibility', 'content')
        }),
        ('System', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Audit Log Admin"""
    list_display = ('actor', 'action', 'member', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('actor__email', 'member__first_name', 'member__last_name', 'action')
    readonly_fields = ('id', 'created_at', 'details')
    
    fieldsets = (
        ('Log Entry', {
            'fields': ('actor', 'member', 'action', 'details')
        }),
        ('System', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
