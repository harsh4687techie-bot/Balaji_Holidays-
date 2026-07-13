import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'balaji_holidays.settings')

application = get_wsgi_application()

# App handle for Vercel
app = application
