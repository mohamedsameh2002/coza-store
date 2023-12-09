release: python manage.py migrate
celery: celery -A PROJECT.celery worker --pool=solo -l info
celerybeat: celery -A PROJECT beat -l info