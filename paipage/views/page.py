__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import json

from django.shortcuts import render, render_to_response
from django.views import View
from django.http import Http404

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt

from paipage import config
from paipage.const import PATH_INDEX, HTML_EXT
from paipage.models import Page

from .params import Params


def make_page(request, params, page, text):
	template = page.template
	if not template:
		template = config.template_page_default
	template += HTML_EXT

	layout = page.layout
	if not layout:
		layout = config.template_layout_default
	layout += HTML_EXT

	params.update({
		'current': page,
		'text': text,
		'upper': page.upper,
		'children': list(page.children.all()),
		'layout_template': layout,
	})
	return render(request, template, params.prepare())


class PageView(View):
	def get(self, request, path=PATH_INDEX):
		params = Params(request)
		lang = params['lang']

		page = Page.objects.filter(url=path).first()
		if page is None:
			raise Http404

		text = page.get_text(lang)
		
		if text is None:
			config.logger.error(f'No lang "{lang}" for page "{path}"')
			layout = config.template_layout_default + HTML_EXT
			params.update({
				'current': page,
				'layout_template': layout,
				'title': config.language_available[params['lang']]['errorNoLang'],
				'description': '',
			})
			return render_to_response('ot-nolang.html', params.prepare())

		else:
			return make_page(request, params, page, text)


@method_decorator(csrf_exempt, name='dispatch')
class PagePreView(View):
	@method_decorator(staff_member_required)
	def post(self, request, ind):
		text = json.loads(request.body.decode('utf-8'))
		params = Params(request)

		page = Page.objects.filter(pk=ind).first()
		if page is None:
			raise Http404

		return make_page(request, params, page, text)
