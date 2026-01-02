# Deployment Guide - Double C Ranch Membership Portal

This guide provides step-by-step instructions for deploying the Double C Ranch Membership Portal to a production environment.

## Prerequisites

Before deploying, ensure you have the following:

- A server with Ubuntu 22.04 or similar Linux distribution
- Python 3.11 or higher installed
- PostgreSQL database server
- Domain name configured and pointing to your server
- SSL certificate (recommended: Let's Encrypt)
- Access to server via SSH

## Deployment Options

### Option 1: Traditional Server Deployment (Recommended)

This approach uses **nginx** as a reverse proxy and **Gunicorn** as the WSGI server.

#### Step 1: Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3.11 python3.11-venv python3-pip postgresql postgresql-contrib nginx git -y

# Install Gunicorn
pip3 install gunicorn
```

#### Step 2: Database Setup

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE ranch_portal;
CREATE USER ranch_user WITH PASSWORD 'your_secure_password_here';
ALTER ROLE ranch_user SET client_encoding TO 'utf8';
ALTER ROLE ranch_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ranch_user SET timezone TO 'America/New_York';
GRANT ALL PRIVILEGES ON DATABASE ranch_portal TO ranch_user;
\q
```

#### Step 3: Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/doublecranch
cd /var/www/doublecranch

# Copy application files
# (Upload your project files here or use git clone)

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

#### Step 4: Environment Configuration

Create `.env` file in the project root:

```env
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=ranch_portal
DB_USER=ranch_user
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=5432
```

#### Step 5: Django Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial documents
python manage.py load_documents

# Collect static files
python manage.py collectstatic --noinput

# Create necessary directories
mkdir -p logs media
```

#### Step 6: Gunicorn Configuration

Create `/etc/systemd/system/ranch_portal.service`:

```ini
[Unit]
Description=Double C Ranch Portal Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/doublecranch
Environment="PATH=/var/www/doublecranch/venv/bin"
ExecStart=/var/www/doublecranch/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/doublecranch/ranch_portal.sock \
          ranch_portal.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable the service:

```bash
sudo systemctl start ranch_portal
sudo systemctl enable ranch_portal
sudo systemctl status ranch_portal
```

#### Step 7: Nginx Configuration

Create `/etc/nginx/sites-available/ranch_portal`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/doublecranch/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/doublecranch/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/doublecranch/ranch_portal.sock;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/ranch_portal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 8: SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### Option 2: Platform-as-a-Service (PaaS) Deployment

#### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create doublecranch-portal
   ```

4. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY='your-secret-key'
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS='.herokuapp.com'
   ```

6. **Create Procfile**
   ```
   web: gunicorn ranch_portal.wsgi --log-file -
   release: python manage.py migrate
   ```

7. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py createsuperuser
   heroku run python manage.py load_documents
   ```

#### DigitalOcean App Platform

1. Connect your GitHub repository
2. Configure build settings:
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Run Command**: `gunicorn ranch_portal.wsgi:application`
3. Add PostgreSQL database
4. Set environment variables
5. Deploy

## Post-Deployment Checklist

### Security

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] SSL/HTTPS enabled
- [ ] Firewall configured (allow only 80, 443, 22)
- [ ] Database password is strong and secure
- [ ] Regular security updates scheduled

### Database

- [ ] Migrations applied
- [ ] Superuser created
- [ ] Initial documents loaded
- [ ] Database backups configured
- [ ] Database connection pooling enabled (if needed)

### Static Files

- [ ] `collectstatic` executed
- [ ] Static files served correctly
- [ ] Media files directory created and writable

### Email Configuration

Update `settings.py` for production email:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@doublecranch.com'
```

### Monitoring & Logging

- [ ] Error logging configured (Sentry recommended)
- [ ] Access logs monitored
- [ ] Performance monitoring enabled
- [ ] Uptime monitoring configured

### Backup Strategy

```bash
# Database backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U ranch_user ranch_portal > /backups/ranch_portal_$DATE.sql
find /backups -name "ranch_portal_*.sql" -mtime +7 -delete
```

Add to crontab:
```bash
0 2 * * * /path/to/backup-script.sh
```

## Maintenance

### Updating the Application

```bash
# Pull latest code
cd /var/www/doublecranch
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart ranch_portal
```

### Database Maintenance

```bash
# Backup database
pg_dump -U ranch_user ranch_portal > backup.sql

# Restore database
psql -U ranch_user ranch_portal < backup.sql

# Vacuum database (optimize)
psql -U ranch_user -d ranch_portal -c "VACUUM ANALYZE;"
```

### Log Management

```bash
# View application logs
sudo journalctl -u ranch_portal -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Rotate logs
sudo logrotate -f /etc/logrotate.d/nginx
```

## Troubleshooting

### Common Issues

**Issue: Static files not loading**
```bash
# Verify static files collected
python manage.py collectstatic --noinput

# Check nginx configuration
sudo nginx -t

# Verify permissions
sudo chown -R www-data:www-data /var/www/doublecranch/staticfiles
```

**Issue: Database connection error**
```bash
# Test database connection
psql -U ranch_user -d ranch_portal -h localhost

# Check PostgreSQL status
sudo systemctl status postgresql

# Verify database credentials in .env
```

**Issue: Gunicorn not starting**
```bash
# Check service status
sudo systemctl status ranch_portal

# View detailed logs
sudo journalctl -u ranch_portal -n 50

# Test Gunicorn manually
cd /var/www/doublecranch
source venv/bin/activate
gunicorn ranch_portal.wsgi:application
```

## Performance Optimization

### Database Optimization

```python
# settings.py - Add database connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

### Caching

```python
# Install Redis
sudo apt install redis-server

# Install Python Redis client
pip install django-redis

# settings.py - Add caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Gunicorn Workers

Adjust workers based on server resources:
```
workers = (2 * CPU_CORES) + 1
```

For a 2-core server: `--workers 5`

## Support

For deployment assistance, contact:
- **Email**: admin@doublecranch.com
- **Phone**: (434) 996-1245

## License

Proprietary - Double C Ranch LLC
