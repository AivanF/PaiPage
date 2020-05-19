__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.shortcuts import render
from django.views import View
from django.http import Http404

from paipage import config
from paipage.const import PATH_INDEX, HTML_EXT
from paipage.models import Page

from .viewUtils import prepare_params


class PageView(View):
	def get(self, request, path=PATH_INDEX):
		params = prepare_params(request)
		lang = params['lang']

		page = Page.objects.filter(url=path).first()
		if page is None:
			raise Http404

		text = page.get_text(lang)
		if text is None:
			config.logger.error(f'No lang "{lang}" for page "{path}"')
			# TODO: show "not available" page
			raise Http404

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
		return render(request, template, params)
