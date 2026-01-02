# Getting Started with Double C Ranch Membership Portal

Welcome to your new membership management system! This guide will help you get started quickly.

## Quick Start (Development)

The application is already running and ready to test at:
**https://8000-icqrvzu0cyq1ryq0zafi5-759e3b84.us2.manus.computer**

### Test Credentials

**Admin/Staff Account:**
- Email: admin@doublecranch.com
- Password: admin123

### Testing the System

#### 1. Test Member Registration
1. Go to the homepage
2. Click "Register"
3. Fill out the registration form
4. Sign the required documents (Liability Waiver and Lesson Agreement)
5. View your member dashboard (status will be "Pending")

#### 2. Test Staff Approval
1. Login as admin (admin@doublecranch.com / admin123)
2. Go to "Staff" → "Manage Members"
3. Find the pending member
4. Click "Approve"

#### 3. Test Check-In
1. Login as the approved member
2. Go to "Check In"
3. Submit a check-in request
4. Login as admin to approve it

#### 4. Test Goal Tracking
1. As a member, go to "My Goals"
2. Submit a goal request
3. As admin, go to Admin Panel → Goals
4. Create an official goal for the member

## What's Included

### Core Features
✅ User registration and authentication
✅ Electronic document signing with audit trail
✅ Member dashboard with statistics
✅ Check-in system with staff approval
✅ Goal tracking and requests
✅ Staff dashboard and member management
✅ Admin interface for all operations
✅ Audit logging for compliance

### Documents Loaded
✅ Liability Waiver and Release of Liability
✅ Riding Lesson Agreement

### User Roles
✅ Member - Can register, sign documents, check in, request goals
✅ Staff - Can approve members, approve check-ins, manage goals
✅ Admin - Full system access including Django admin

## File Structure

```
double-c-ranch-portal/
├── README.md                    # Complete documentation
├── DEPLOYMENT.md                # Production deployment guide
├── PROJECT_SUMMARY.md           # Project overview
├── GETTING_STARTED.md          # This file
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management script
├── db.sqlite3                   # Database (development)
├── ranch_portal/                # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── members/                     # Main application
│   ├── models.py               # 10 database models
│   ├── views.py                # All views
│   ├── forms.py                # All forms
│   ├── urls.py                 # URL routing
│   ├── admin.py                # Admin configuration
│   └── management/
│       └── commands/
│           └── load_documents.py
├── templates/                   # HTML templates
│   ├── base.html
│   ├── portal/                 # Member templates
│   ├── staff/                  # Staff templates
│   └── registration/           # Auth templates
└── static/
    └── css/
        └── custom.css          # Custom styling
```

## Key URLs

### Public
- `/` - Homepage
- `/register/` - Member registration
- `/accounts/login/` - Login
- `/accounts/logout/` - Logout

### Member (Requires Login)
- `/dashboard/` - Member dashboard
- `/sign-documents/` - Sign required documents
- `/checkin/` - Submit check-in
- `/goals/` - View and request goals
- `/profile/` - Member profile

### Staff (Requires Staff Role)
- `/staff/` - Staff dashboard
- `/staff/members/` - Manage members
- `/staff/checkins/` - Manage check-ins

### Admin (Requires Admin Role)
- `/admin/` - Django admin interface

## Next Steps

### For Immediate Use

1. **Create Staff Accounts**
   - Go to Admin → Users → Add User
   - Create accounts for your staff
   - Add them to the "Staff" group

2. **Customize Documents**
   - Go to Admin → Documents
   - Edit the existing documents or add new ones

3. **Test the Complete Workflow**
   - Register → Sign Documents → Check In → Request Goals
   - Approve as staff

### For Production Deployment

1. **Read DEPLOYMENT.md** - Complete deployment guide
2. **Choose a hosting provider** (DigitalOcean, AWS, Heroku)
3. **Set up PostgreSQL database**
4. **Configure environment variables**
5. **Set up SSL certificate**
6. **Configure email SMTP**
7. **Test thoroughly**
8. **Go live!**

## Common Tasks

### Adding a New Document
```bash
python manage.py shell
```
```python
from members.models import Document

Document.objects.create(
    code='NEW_DOC',
    name='New Document Name',
    version=1,
    content='Document content here...',
    is_active=True,
    is_required=True
)
```

### Creating a Staff User
1. Go to `/admin/auth/user/add/`
2. Create the user
3. Edit the user and add to "Staff" group
4. Check "Staff status"

### Viewing Audit Logs
1. Go to `/admin/members/auditlog/`
2. Filter by action, date, or member

### Backing Up Database
```bash
# SQLite (development)
cp db.sqlite3 db.sqlite3.backup

# PostgreSQL (production)
pg_dump -U ranch_user ranch_portal > backup.sql
```

## Customization

### Changing Colors/Branding
Edit `static/css/custom.css`:
```css
:root {
    --primary-color: #2c5530;  /* Your brand color */
    --secondary-color: #8b4513;
    --accent-color: #d4af37;
}
```

### Adding Email Notifications
Update `ranch_portal/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Changing Membership Tiers
Edit `members/models.py` → `Member.MEMBERSHIP_TIERS`

## Support

### Documentation
- **README.md** - Complete feature documentation
- **DEPLOYMENT.md** - Production deployment guide
- **PROJECT_SUMMARY.md** - Technical overview

### Contact
- **Location**: 2626 Yule Farm, Charlottesville, VA 22901
- **Phone**: (434) 996-1245
- **Company**: Double C Ranch LLC

## Troubleshooting

### Server Not Starting
```bash
cd /home/ubuntu/double-c-ranch-portal
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### Database Issues
```bash
python manage.py migrate
python manage.py load_documents
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Reset Admin Password
```bash
python manage.py changepassword admin@doublecranch.com
```

## Security Reminders

⚠️ **Before Going to Production:**
1. Change the admin password from "admin123"
2. Set `DEBUG=False` in settings
3. Generate a new `SECRET_KEY`
4. Enable HTTPS/SSL
5. Configure proper database backups
6. Set up email notifications
7. Review all user permissions

## Success Checklist

✅ System is running
✅ Admin account works
✅ Can register new members
✅ Documents are loading
✅ Can sign documents
✅ Check-in system works
✅ Staff approval works
✅ Goals system works
✅ Admin interface accessible

## You're All Set!

The Double C Ranch Membership Portal is ready to use. Start by testing the complete workflow, then customize it to your needs. When you're ready for production, follow the DEPLOYMENT.md guide.

Happy riding! 🐴
