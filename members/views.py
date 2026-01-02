"""
Views for Double C Ranch Portal
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime, timedelta

from .models import (
    User, Member, Document, SignedDocument,
    CheckIn, Goal, GoalUpdate, GoalRequest, Note, AuditLog
)
from .forms import (
    RegistrationForm, SignDocumentForm, CheckInForm,
    GoalForm, GoalUpdateForm, GoalRequestForm, NoteForm,
    MemberApprovalForm, StaffCheckInForm, MemberSearchForm
)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_staff(user):
    """Check if user is staff"""
    return user.is_staff_user if hasattr(user, 'is_staff_user') else user.is_staff


def is_admin(user):
    """Check if user is admin"""
    return user.is_admin_user if hasattr(user, 'is_admin_user') else user.is_superuser


# ============================================================================
# PUBLIC VIEWS
# ============================================================================

def home(request):
    """Landing page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'portal/home.html')


def register(request):
    """Member registration - Step 1: Create account"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()
            
            # Create member profile
            member = Member.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                parent_name=form.cleaned_data.get('parent_name', ''),
                phone=form.cleaned_data['phone'],
                membership_tier=form.cleaned_data['membership_tier'],
                status='Pending'
            )
            
            # Log audit
            AuditLog.log('Member Registration', actor=user, member=member)
            
            # Log in the user
            login(request, user)
            
            messages.success(request, 'Account created! Please sign the required documents.')
            return redirect('sign_documents')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


# ============================================================================
# MEMBER VIEWS
# ============================================================================

@login_required
def dashboard(request):
    """Member dashboard"""
    try:
        member = request.user.member_profile
    except:
        messages.error(request, 'Member profile not found.')
        return redirect('home')
    
    # Get recent check-ins
    recent_checkins = member.checkins.all()[:5]
    
    # Get active goals
    active_goals = member.goals.filter(status__in=['NotStarted', 'InProgress'])
    
    # Get recent notes (student-visible only)
    recent_notes = member.notes.filter(visibility='StudentVisible')[:5]
    
    # Check if documents are signed
    needs_documents = not member.has_signed_all_required_documents()
    
    context = {
        'member': member,
        'recent_checkins': recent_checkins,
        'active_goals': active_goals,
        'recent_notes': recent_notes,
        'needs_documents': needs_documents,
    }
    
    return render(request, 'portal/dashboard.html', context)


@login_required
def sign_documents(request):
    """Sign required documents"""
    try:
        member = request.user.member_profile
    except:
        messages.error(request, 'Member profile not found.')
        return redirect('home')
    
    # Get all required active documents
    required_docs = Document.objects.filter(is_active=True, is_required=True)
    
    # Get documents already signed by this member
    signed_doc_ids = SignedDocument.objects.filter(
        member=member
    ).values_list('document_id', flat=True)
    
    # Get unsigned documents
    unsigned_docs = required_docs.exclude(id__in=signed_doc_ids)
    
    if not unsigned_docs.exists():
        messages.info(request, 'All required documents have been signed.')
        return redirect('dashboard')
    
    # Get the first unsigned document
    document = unsigned_docs.first()
    
    if request.method == 'POST':
        form = SignDocumentForm(request.POST)
        if form.is_valid():
            # Create signed document record
            SignedDocument.objects.create(
                document=document,
                member=member,
                user=request.user,
                signed_name=form.cleaned_data['signed_name'],
                signed_for_name=form.cleaned_data.get('signed_for_name', ''),
                relationship=form.cleaned_data.get('relationship', ''),
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                document_snapshot=document.content
            )
            
            # Log audit
            AuditLog.log(
                f'Document Signed: {document.name}',
                actor=request.user,
                member=member
            )
            
            messages.success(request, f'Document "{document.name}" signed successfully.')
            
            # Check if there are more documents to sign
            if unsigned_docs.count() > 1:
                return redirect('sign_documents')
            else:
                messages.success(request, 'All required documents signed! Your membership is pending approval.')
                return redirect('dashboard')
    else:
        form = SignDocumentForm()
    
    context = {
        'document': document,
        'form': form,
        'remaining': unsigned_docs.count(),
        'total': required_docs.count()
    }
    
    return render(request, 'portal/sign_document.html', context)


@login_required
def checkin(request):
    """Member check-in"""
    try:
        member = request.user.member_profile
    except:
        messages.error(request, 'Member profile not found.')
        return redirect('home')
    
    if member.status != 'Approved':
        messages.warning(request, 'Your membership is pending approval.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.member = member
            checkin.created_by = request.user
            checkin.save()
            
            # Log audit
            AuditLog.log(
                f'Check-in Requested: {checkin.type}',
                actor=request.user,
                member=member
            )
            
            messages.success(request, 'Check-in submitted! Waiting for staff approval.')
            return redirect('dashboard')
    else:
        form = CheckInForm()
    
    # Get recent check-ins
    recent_checkins = member.checkins.all()[:10]
    
    context = {
        'form': form,
        'recent_checkins': recent_checkins
    }
    
    return render(request, 'portal/checkin.html', context)


@login_required
def goals(request):
    """View and request goals"""
    try:
        member = request.user.member_profile
    except:
        messages.error(request, 'Member profile not found.')
        return redirect('home')
    
    # Get member's goals
    member_goals = member.goals.all()
    
    # Get goal requests
    goal_requests = member.goal_requests.all()
    
    if request.method == 'POST':
        form = GoalRequestForm(request.POST)
        if form.is_valid():
            goal_request = form.save(commit=False)
            goal_request.member = member
            goal_request.submitted_by = request.user
            goal_request.save()
            
            messages.success(request, 'Goal request submitted!')
            return redirect('goals')
    else:
        form = GoalRequestForm()
    
    context = {
        'member_goals': member_goals,
        'goal_requests': goal_requests,
        'form': form
    }
    
    return render(request, 'portal/goals.html', context)


@login_required
def profile(request):
    """View member profile"""
    try:
        member = request.user.member_profile
    except:
        messages.error(request, 'Member profile not found.')
        return redirect('home')
    
    # Get signed documents
    signed_docs = member.signed_documents.all()
    
    context = {
        'member': member,
        'signed_docs': signed_docs
    }
    
    return render(request, 'portal/profile.html', context)


# ============================================================================
# STAFF VIEWS
# ============================================================================

@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    """Staff dashboard"""
    # Pending approvals
    pending_members = Member.objects.filter(status='Pending').count()
    pending_checkins = CheckIn.objects.filter(status='Pending').count()
    open_goal_requests = GoalRequest.objects.filter(status='Open').count()
    
    # Recent activity
    recent_checkins = CheckIn.objects.select_related('member').all()[:10]
    recent_members = Member.objects.all()[:10]
    
    context = {
        'pending_members': pending_members,
        'pending_checkins': pending_checkins,
        'open_goal_requests': open_goal_requests,
        'recent_checkins': recent_checkins,
        'recent_members': recent_members,
    }
    
    return render(request, 'staff/dashboard.html', context)


@login_required
@user_passes_test(is_staff)
def staff_members(request):
    """Staff member management"""
    form = MemberSearchForm(request.GET)
    members = Member.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        status = form.cleaned_data.get('status')
        tier = form.cleaned_data.get('membership_tier')
        
        if query:
            members = members.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(phone__icontains=query) |
                Q(user__email__icontains=query)
            )
        
        if status:
            members = members.filter(status=status)
        
        if tier:
            members = members.filter(membership_tier=tier)
    
    context = {
        'members': members,
        'form': form
    }
    
    return render(request, 'staff/members.html', context)


@login_required
@user_passes_test(is_staff)
def staff_member_detail(request, member_id):
    """Staff view of member details"""
    member = get_object_or_404(Member, id=member_id)
    
    # Get all related data
    checkins = member.checkins.all()
    goals = member.goals.all()
    notes = member.notes.all()
    signed_docs = member.signed_documents.all()
    
    context = {
        'member': member,
        'checkins': checkins,
        'goals': goals,
        'notes': notes,
        'signed_docs': signed_docs,
    }
    
    return render(request, 'staff/member_detail.html', context)


@login_required
@user_passes_test(is_staff)
def staff_approve_member(request, member_id):
    """Approve a member"""
    member = get_object_or_404(Member, id=member_id)
    member.status = 'Approved'
    member.save()
    
    # Log audit
    AuditLog.log(
        'Member Approved',
        actor=request.user,
        member=member
    )
    
    messages.success(request, f'{member.full_name} has been approved.')
    return redirect('staff_members')


@login_required
@user_passes_test(is_staff)
def staff_checkins(request):
    """Staff check-in management"""
    checkins = CheckIn.objects.select_related('member', 'created_by').all()[:50]
    
    context = {
        'checkins': checkins
    }
    
    return render(request, 'staff/checkins.html', context)


@login_required
@user_passes_test(is_staff)
def staff_approve_checkin(request, checkin_id):
    """Approve a check-in"""
    checkin = get_object_or_404(CheckIn, id=checkin_id)
    checkin.approve(request.user)
    
    messages.success(request, 'Check-in approved.')
    return redirect('staff_checkins')
