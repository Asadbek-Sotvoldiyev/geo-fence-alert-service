from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi


UNFOLD = {
    "SITE_TITLE": "Geo-Fence",
    "SITE_HEADER": "Geo-Fence alert service",
    "SITE_URL": "/",
    "SITE_SYMBOL": "speed",
}


import logging.config


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log', 
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING)


schema_view = get_schema_view(
    openapi.Info(
        title="FarGenius Group",
        default_version='v1',
        description="FarGenius Group",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)