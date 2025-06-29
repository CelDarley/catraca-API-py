"""
WSGI config for rasp_api project - Production
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rasp_api.settings_prod')

application = get_wsgi_application() 