import os
import django.core.handlers.wsgi

os.environ['PYTHON_EGG_CACHE'] = '/tmp/cs_egg_cache'
os.environ['DJANGO_SETTINGS_MODULE'] = 'churchsource.settings'
application = django.core.handlers.wsgi.WSGIHandler()

