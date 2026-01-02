"""
Forms for Double C Ranch Portal
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User, Member, SignedDocument, CheckIn,
    Goal, GoalRequest, GoalUpdate, Note
)


class RegistrationForm(UserCreationForm):
    """User registration form"""
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    parent_name = forms.CharField(max_length=200, required=False, 
                                 help_text="Required if rider is under 18")
    phone = forms.CharField(max_length=50, required=True)
    membership_tier = forms.ChoiceField(choices=Member.MEMBERSHIP_TIERS, 
                                       initial='Lesson')
    
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 
                 'parent_name', 'phone', 'membership_tier')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['parent_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Parent/Guardian Name (if under 18)'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone Number'})
        self.fields['membership_tier'].widget.attrs.update({'class': 'form-select'})


class SignDocumentForm(forms.Form):
    """Form for signing documents"""
    signed_name = forms.CharField(
        max_length=200,
        required=True,
        label="Legal Name (Type to Sign)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type your full legal name'
        })
    )
    signed_for_name = forms.CharField(
        max_length=200,
        required=False,
        label="Student Name (if signing for someone else)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Student name'
        })
    )
    relationship = forms.CharField(
        max_length=100,
        required=False,
        label="Relationship (if signing for someone else)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parent, Guardian, etc.'
        })
    )
    agree = forms.BooleanField(
        required=True,
        label="I have read and agree to the terms and conditions",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class CheckInForm(forms.ModelForm):
    """Form for member check-in"""
    class Meta:
        model = CheckIn
        fields = ('type', 'student_note')
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'student_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional note for staff'
            })
        }


class StaffCheckInForm(forms.ModelForm):
    """Form for staff to manage check-ins"""
    class Meta:
        model = CheckIn
        fields = ('status', 'instructor', 'staff_note')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'instructor': forms.Select(attrs={'class': 'form-select'}),
            'staff_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Staff notes'
            })
        }


class GoalRequestForm(forms.ModelForm):
    """Form for members to request goals"""
    class Meta:
        model = GoalRequest
        fields = ('content', 'timeframe')
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your goal'
            }),
            'timeframe': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 3 months, 6 months, 1 year'
            })
        }


class GoalForm(forms.ModelForm):
    """Form for staff to create/edit goals"""
    class Meta:
        model = Goal
        fields = ('title', 'description', 'target_date', 'status')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Goal title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Goal description'
            }),
            'target_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-select'})
        }


class GoalUpdateForm(forms.ModelForm):
    """Form for adding goal updates"""
    class Meta:
        model = GoalUpdate
        fields = ('note',)
        widgets = {
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Progress update'
            })
        }


class NoteForm(forms.ModelForm):
    """Form for instructor notes"""
    class Meta:
        model = Note
        fields = ('category', 'visibility', 'content')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'visibility': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Note content'
            })
        }


class MemberApprovalForm(forms.ModelForm):
    """Form for staff to approve/manage members"""
    class Meta:
        model = Member
        fields = ('status', 'membership_tier', 'certification_level')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'membership_tier': forms.Select(attrs={'class': 'form-select'}),
            'certification_level': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Certification level'
            })
        }


class MemberSearchForm(forms.Form):
    """Form for searching members"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, email, or phone'
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + Member.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    membership_tier = forms.ChoiceField(
        required=False,
        choices=[('', 'All Tiers')] + Member.MEMBERSHIP_TIERS,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
