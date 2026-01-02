# Double C Ranch Membership Portal

A comprehensive Django-based membership management system for Double C Ranch / Pony Club Riding Center.

## Project Overview

This portal provides a complete solution for managing riding lessons, memberships, document signing, check-ins, goal tracking, and more.

### Key Features

1. **User Authentication & Registration**
   - Email-based authentication using Django Allauth
   - Member registration with profile creation
   - Role-based access control (Member, Staff, Admin)

2. **Document Management & E-Signing**
   - Digital waiver and liability release forms
   - Riding lesson agreement
   - Electronic signature with audit trail (IP, timestamp, user agent)
   - Document versioning support

3. **Member Dashboard**
   - Attendance tracking (30-day and all-time)
   - Active goals display
   - Recent check-ins
   - Instructor notes (student-visible)
   - Quick actions (check-in, schedule lessons, view goals)

4. **Check-In System**
   - Student-initiated check-in requests
   - Staff approval workflow
   - Check-in types: Lesson, Horsemanship, Camp, Event, Other
   - Automatic attendance statistics updates

5. **Goal Tracking**
   - Members can request goals
   - Staff creates official goals
   - Progress updates from both staff and members
   - Goal status tracking (Not Started, In Progress, Complete)

6. **Staff Dashboard**
   - Pending member approvals
   - Pending check-in approvals
   - Open goal requests
   - Member search and management
   - Detailed member profiles with full history

7. **Admin Interface**
   - Full Django admin for all models
   - Bulk actions for approvals
   - Document management
   - Audit log viewing

8. **Audit Trail**
   - Complete activity logging
   - Track all important actions
   - Compliance and legal record keeping

## Technology Stack

- **Backend**: Django 4.2
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Authentication**: Django Allauth
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Python**: 3.11

## Installation & Setup

### Prerequisites

- Python 3.11
- pip
- virtualenv

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd /home/ubuntu/double-c-ranch-portal
   ```

2. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies** (already installed)
   ```bash
   pip install django django-allauth django-crispy-forms crispy-bootstrap5 python-decouple
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load initial documents**
   ```bash
   python manage.py load_documents
   ```

6. **Create superuser** (already created)
   ```bash
   python manage.py createsuperuser
   ```
   - Email: admin@doublecranch.com
   - Password: admin123

7. **Run development server**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Database Models

### User
- Custom user model extending AbstractUser
- Email-based authentication
- Role properties (is_member, is_staff_user, is_admin_user)

### Member
- Member profile linked to User
- Status: Pending, Approved, Disabled, Merged
- Membership tiers: Lesson, Horsemanship, Camp, Event, Other
- Attendance tracking
- Certification level

### Document
- Document templates (waivers, agreements)
- Versioning support
- Active/inactive status
- Required/optional flag

### SignedDocument
- Record of member signatures
- Document snapshot at time of signing
- IP address and user agent tracking
- Legal audit trail

### CheckIn
- Student check-in requests
- Staff approval workflow
- Types: Lesson, Horsemanship, Camp, Event, Other
- Status: Pending, Confirmed, Rejected
- Instructor assignment

### Goal & GoalRequest
- Member goal requests
- Staff-created official goals
- Progress tracking
- Target dates

### GoalUpdate
- Progress updates on goals
- Author type (Staff/Member)
- Chronological history

### Note
- Instructor notes for members
- Categories: Riding, Horsemanship, Safety, Behavior, Admin
- Visibility: Student Visible, Staff Only

### AuditLog
- System-wide audit trail
- Action tracking
- JSON details field

## User Roles & Permissions

### Member
- Register and create account
- Sign required documents
- View personal dashboard
- Submit check-in requests
- Request goals
- View student-visible notes
- View personal profile and signed documents

### Staff
- All Member permissions
- Approve/reject member registrations
- Approve/reject check-ins
- Create and manage goals
- Add notes (student-visible and staff-only)
- View all member details
- Search and filter members

### Admin
- All Staff permissions
- Full Django admin access
- Manage documents
- View audit logs
- System configuration

## URL Structure

### Public URLs
- `/` - Homepage
- `/register/` - Member registration
- `/accounts/login/` - Login
- `/accounts/logout/` - Logout

### Member URLs
- `/dashboard/` - Member dashboard
- `/sign-documents/` - Document signing workflow
- `/checkin/` - Check-in submission
- `/goals/` - View and request goals
- `/profile/` - Member profile

### Staff URLs
- `/staff/` - Staff dashboard
- `/staff/members/` - Member management
- `/staff/members/<id>/` - Member detail view
- `/staff/members/<id>/approve/` - Approve member
- `/staff/checkins/` - Check-in management
- `/staff/checkins/<id>/approve/` - Approve check-in

### Admin URLs
- `/admin/` - Django admin interface

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=ranch_portal
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### Settings

Key settings in `ranch_portal/settings.py`:

- `AUTH_USER_MODEL = 'members.User'` - Custom user model
- `TIME_ZONE = 'America/New_York'` - Eastern Time
- `ACCOUNT_AUTHENTICATION_METHOD = 'email'` - Email-based auth
- `LOGIN_REDIRECT_URL = '/dashboard/'` - Post-login redirect

## Management Commands

### load_documents
Loads initial required documents (liability waiver and lesson agreement) into the database.

```bash
python manage.py load_documents
```

## Integration Points

### Acuity Scheduling
The portal includes links to Acuity Scheduling for lesson booking:
- URL: https://app.acuityscheduling.com/catalog.php?owner=36970923&action=addCart&clear=1&id=2073271
- Note: Rescheduling should be done via email confirmation link (24-hour notice required)

### Future Integrations
- Email notifications (currently using console backend)
- SMS notifications for check-in approvals
- Payment processing integration
- Calendar sync (Google Calendar, Outlook)
- Automated attendance reports

## Security Features

1. **CSRF Protection** - All forms protected
2. **Password Validation** - Django's built-in validators
3. **Electronic Signature Audit** - IP, timestamp, user agent tracking
4. **Document Snapshots** - Immutable legal records
5. **Audit Logging** - Complete activity trail
6. **Role-Based Access Control** - Permission checks on all views

## Testing

### Admin Access
- Email: admin@doublecranch.com
- Password: admin123
- URL: https://8000-icqrvzu0cyq1ryq0zafi5-759e3b84.us2.manus.computer/admin/

### Test Workflow

1. **Register a new member**
   - Go to /register/
   - Fill out registration form
   - Sign required documents
   - View dashboard (status: Pending)

2. **Staff approval**
   - Login as admin
   - Go to /staff/members/
   - Approve the member

3. **Member check-in**
   - Login as member
   - Go to /checkin/
   - Submit check-in request

4. **Staff approval**
   - Login as staff
   - Go to /staff/checkins/
   - Approve check-in

## File Structure

```
double-c-ranch-portal/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
├── ranch_portal/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── members/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── migrations/
│   └── management/
│       └── commands/
│           └── load_documents.py
├── templates/
│   ├── base.html
│   ├── portal/
│   │   ├── home.html
│   │   ├── dashboard.html
│   │   ├── sign_document.html
│   │   ├── checkin.html
│   │   ├── goals.html
│   │   └── profile.html
│   ├── staff/
│   │   ├── dashboard.html
│   │   ├── members.html
│   │   ├── member_detail.html
│   │   └── checkins.html
│   └── registration/
│       ├── register.html
│       └── login.html
└── static/
    └── css/
        └── custom.css
```

## Deployment Considerations

### Production Checklist

1. **Environment**
   - Set `DEBUG=False`
   - Use PostgreSQL database
   - Set strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`

2. **Security**
   - Enable HTTPS
   - Set secure cookie flags
   - Configure CSRF trusted origins
   - Set up proper firewall rules

3. **Static Files**
   - Run `python manage.py collectstatic`
   - Serve via nginx or CDN

4. **Database**
   - Set up PostgreSQL
   - Configure backups
   - Run migrations

5. **Email**
   - Configure SMTP settings
   - Set up email templates

6. **Monitoring**
   - Set up error logging
   - Configure Sentry or similar
   - Monitor database performance

## Support & Maintenance

### Contact Information
- **Location**: 2626 Yule Farm, Charlottesville, VA 22901
- **Phone**: (434) 996-1245
- **Company**: Double C Ranch LLC

### Maintenance Tasks

- Regular database backups
- Monitor audit logs
- Review pending approvals
- Update documents as needed
- Check system logs for errors

## License

Proprietary - Double C Ranch LLC

## Version History

- **v1.0** (January 2026) - Initial release
  - User authentication and registration
  - Document signing system
  - Check-in management
  - Goal tracking
  - Staff dashboard
  - Admin interface
  - Audit logging
