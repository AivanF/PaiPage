__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.PageView.as_view()),
	path('<slug:path>', views.PageView.as_view()),
	path('_lang/<slug:lang>', views.ChangeLangView.as_view()),

	path('adminka/structure', views.StructureView.as_view()),
]
