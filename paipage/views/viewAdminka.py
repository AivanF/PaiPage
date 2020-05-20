__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.shortcuts import render
from django.views import View

from paipage import config
from paipage.models import Page

from .viewUtils import Params


# TODO: check user is_staff
class StructureView(View):
	def get(self, request):
		params = Params(request)
		params['layout_template'] = 'lo-pure.html'
		params.scripted['all_pages'] = Page.get_all()
		params.scripted['language_selectable'] =list(config.language_available.keys())
		return render(request, 'am-struct.html', params.prepare())
