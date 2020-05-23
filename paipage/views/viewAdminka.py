__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import json

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from paipage import config
from paipage.models import Page

from .viewUtils import Params


class StructureView(View):
	@method_decorator(staff_member_required)
	def get(self, request):
		params = Params(request)
		params.scripted['all_pages'] = Page.get_all()
		params.scripted['language_selectable'] = list(config.language_available.keys())
		params.scripted['default_page'] = config.template_page_default
		params.scripted['default_layout'] = config.template_layout_default
		params.selectables['template_layout'] = ['lo-pure', 'lo-menu-left', 'lo-menu-top']
		params.selectables['template_page'] = ['pg-pure', 'pg-usual', 'pg-cluster']
		return render(request, 'am-struct.html', params.prepare())


class AdminkaPageView(View):
	@method_decorator(staff_member_required)
	def get(self, request, pk):
		page = get_object_or_404(Page, pk=pk)

	@method_decorator(staff_member_required)
	def post(self, request, pk):
		j = json.loads(request.body.decode('utf-8'))
		page = get_object_or_404(Page, pk=pk)

		print(page, j)
		res = {
			'success': True,
			'comment': '-',
		}

		if res['success']:
			new_url = j['url']
			if new_url != page.url:
				other = Page.objects.filter(url=new_url).first()
				if other is not None:
					res['success'] = False
					res['comment'] = 'The address is already in use'
				else:
					page.url = new_url

		if res['success']:
			new_upper = int(j['upper'])
			if new_upper != page.upper:
				if new_upper == pk:
					res['success'] = False
					res['comment'] = 'Cannot link page to itself'
				if new_upper != None:
					temp_upper = new_upper
					while True:
						if temp_upper is None:
							break
						temp = get_object_or_404(Page, pk=temp_upper)
						if temp.upper:
							temp_upper = temp.upper.pk
						else:
							break
						if temp_upper == new_upper:
							break  # prevent looping
						if pk == temp_upper:
							res['success'] = False
							res['comment'] = 'Cannot link page to itself'
				page.upper = get_object_or_404(Page, pk=new_upper)

		if res['success']:
			page.layout = j['template_layout']
			page.layout = '' if page.layout is None else page.layout
			page.template = j['template_page']
			page.template = '' if page.template is None else page.template

		if res['success']:
			page.updated_by = request.user
			page.save()

		return HttpResponse(json.dumps(res))


class AdminkaPageTextView(View):
	@method_decorator(staff_member_required)
	def post(self, request, pk, lang):
		j = json.loads(request.body.decode('utf-8'))
		page = get_object_or_404(Page, pk=pk)
		text = page.get_text(lang)
		if text is None:
			# Create new
			pass
		# TODO: check that new_lang == old_lang or new_lang not created yet
