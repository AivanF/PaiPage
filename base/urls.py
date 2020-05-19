__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('paipage.urls')),
]
