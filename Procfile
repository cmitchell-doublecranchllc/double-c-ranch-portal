web: gunicorn ranch_portal.wsgi --log-file -
release: python manage.py migrate && python manage.py load_documents
