__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.shortcuts import render
from django.views import View

from paipage import config
from paipage.models import Page

from .viewUtils import prepare_params


class StructureView(View):
	def get(self, request):
		params = prepare_params(request)
		print(list(Page.objects.all()))
		return render(request, 'am-struct.html', params)


class EditView(View):
	def get(self, request, path=None):
		print('EditView')
		pass
