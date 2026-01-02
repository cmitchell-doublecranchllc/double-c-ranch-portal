"""
Double C Ranch / Pony Club Riding Center
Membership Portal - Data Models
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import EmailValidator


class User(AbstractUser):
    """
    Extended User model for authentication
    Supports Member, Staff, and Admin roles
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    email_verified_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Override username to use email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def is_member(self):
        return self.groups.filter(name='Member').exists()

    @property
    def is_staff_user(self):
        return self.groups.filter(name='Staff').exists() or self.is_superuser

    @property
    def is_admin_user(self):
        return self.is_superuser or self.groups.filter(name='Admin').exists()


class Member(models.Model):
    """
    Member profile - represents a student/rider
    Linked to User account after approval
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending Approval'),
        ('Approved', 'Approved'),
        ('Disabled', 'Disabled'),
        ('Merged', 'Merged'),
    ]

    MEMBERSHIP_TIERS = [
        ('Lesson', 'Lesson Member'),
        ('Horsemanship', 'Horsemanship Member'),
        ('Camp', 'Camp Member'),
        ('Event', 'Event Member'),
        ('Other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True, related_name='member_profile')

    # Basic Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    # Membership Details
    membership_tier = models.CharField(max_length=100, choices=MEMBERSHIP_TIERS, default='Lesson')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    certification_level = models.CharField(max_length=100, blank=True, default='None')

    # Merge tracking
    merged_into = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='merged_members')

    # Denormalized stats for performance
    attendance_30d = models.IntegerField(default=0)
    attendance_all_time = models.IntegerField(default=0)
    last_checkin_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'members'
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_approved(self):
        return self.status == 'Approved'

    @property
    def is_pending(self):
        return self.status == 'Pending'

    def has_signed_all_required_documents(self):
        """Check if member has signed all required active documents"""
        required_docs = Document.objects.filter(is_active=True, is_required=True)
        signed_docs = SignedDocument.objects.filter(member=self).values_list('document_id', flat=True)
        return all(doc.id in signed_docs for doc in required_docs)


class Document(models.Model):
    """
    Document templates (Lesson Agreement, Liability Release, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    version = models.IntegerField(default=1)
    content = models.TextField(help_text="Full text of the document")
    is_active = models.BooleanField(default=True)
    is_required = models.BooleanField(default=True, help_text="Must be signed during registration")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'documents'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['code', '-version']
        unique_together = ['code', 'version']

    def __str__(self):
        return f"{self.name} (v{self.version})"


class SignedDocument(models.Model):
    """
    Record of a member signing a document
    Stores snapshot of document content at time of signing
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.PROTECT, related_name='signatures')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='signed_documents')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='signed_documents')

    # Signature details
    signed_name = models.CharField(max_length=200, help_text="Legal name typed as signature")
    signed_for_name = models.CharField(max_length=200, blank=True, help_text="Student name if parent is signing")
    relationship = models.CharField(max_length=100, blank=True, help_text="Parent, Guardian, etc.")

    # Audit trail
    signed_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    # Legal record - exact text they agreed to
    document_snapshot = models.TextField(help_text="Exact document content at time of signing")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'signed_documents'
        verbose_name = 'Signed Document'
        verbose_name_plural = 'Signed Documents'
        ordering = ['-signed_at']
        unique_together = ['document', 'member']

    def __str__(self):
        return f"{self.member.full_name} - {self.document.name} - {self.signed_at.date()}"


class CheckIn(models.Model):
    """
    Student check-in records
    Requires staff approval
    """
    TYPE_CHOICES = [
        ('Lesson', 'Lesson'),
        ('Horsemanship', 'Horsemanship'),
        ('Camp', 'Camp'),
        ('Event', 'Event'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='checkins')

    # Check-in details
    requested_at = models.DateTimeField(default=timezone.now)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Lesson')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # Notes
    student_note = models.CharField(max_length=255, blank=True)
    staff_note = models.CharField(max_length=255, blank=True)

    # Assignment
    instructor = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_checkins')

    # Audit
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_checkins')
    approved_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_checkins')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'checkins'
        verbose_name = 'Check-In'
        verbose_name_plural = 'Check-Ins'
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.member.full_name} - {self.type} - {self.requested_at.date()}"

    def approve(self, staff_user, instructor=None):
        """Approve check-in and update member stats"""
        self.status = 'Confirmed'
        self.confirmed_at = timezone.now()
        self.approved_by = staff_user
        if instructor:
            self.instructor = instructor
        self.save()
        
        # Update member stats
        self.member.last_checkin_at = self.confirmed_at
        self.member.attendance_all_time += 1
        self.member.save()


class GoalRequest(models.Model):
    """
    Student-submitted goal requests
    Staff reviews and creates official Goals
    """
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Processed', 'Processed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='goal_requests')
    submitted_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='submitted_goal_requests')

    content = models.TextField()
    timeframe = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goal_requests'
        verbose_name = 'Goal Request'
        verbose_name_plural = 'Goal Requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member.full_name} - {self.timeframe}"


class Goal(models.Model):
    """
    Official goals created by staff for members
    """
    STATUS_CHOICES = [
        ('NotStarted', 'Not Started'),
        ('InProgress', 'In Progress'),
        ('Complete', 'Complete'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='goals')
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_goals')

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NotStarted')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goals'
        verbose_name = 'Goal'
        verbose_name_plural = 'Goals'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member.full_name} - {self.title}"

    @property
    def latest_update(self):
        return self.updates.first()


class GoalUpdate(models.Model):
    """
    Progress updates on goals
    Can be added by staff or members
    """
    AUTHOR_TYPE_CHOICES = [
        ('Staff', 'Staff'),
        ('Member', 'Member'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='updates')
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='goal_updates')
    author_type = models.CharField(max_length=20, choices=AUTHOR_TYPE_CHOICES)

    note = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'goal_updates'
        verbose_name = 'Goal Update'
        verbose_name_plural = 'Goal Updates'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.goal.title} - {self.created_at.date()}"


class Note(models.Model):
    """
    Instructor notes for members
    Two visibility levels: Student-visible and Staff-only
    """
    CATEGORY_CHOICES = [
        ('Riding', 'Riding'),
        ('Horsemanship', 'Horsemanship'),
        ('Safety', 'Safety'),
        ('Behavior', 'Behavior'),
        ('Admin', 'Admin'),
    ]

    VISIBILITY_CHOICES = [
        ('StudentVisible', 'Student Visible'),
        ('StaffOnly', 'Staff Only'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='authored_notes')

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notes'
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.member.full_name} - {self.category} - {self.created_at.date()}"


class AuditLog(models.Model):
    """
    System audit trail
    Tracks all important actions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_actions')
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')

    action = models.CharField(max_length=100)
    details = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_log'
        verbose_name = 'Audit Log Entry'
        verbose_name_plural = 'Audit Log'
        ordering = ['-created_at']

    def __str__(self):
        actor_name = self.actor.email if self.actor else 'System'
        return f"{actor_name} - {self.action} - {self.created_at}"

    @classmethod
    def log(cls, action, actor=None, member=None, details=None):
        """Convenience method to create audit log entries"""
        return cls.objects.create(
            action=action,
            actor=actor,
            member=member,
            details=details or {}
        )
