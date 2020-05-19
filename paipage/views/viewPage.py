__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.shortcuts import render
from django.views import View
from django.http import Http404

from paipage import config
from paipage.const import PATH_INDEX
from paipage.models import Page

from .viewUtils import prepare_params


class PageView(View):
	def get(self, request, path=PATH_INDEX):
		params = prepare_params(request)

		page = Page.objects.filter(url=path).first()
		if page is None:
			raise Http404

		text = page.get_text(params['lang'])
		if text is None:
			config.logger.error(f'No lang "{lang}" for page "{path}"')
			# TODO: show "not available" page
			raise Http404

		params.update({
			'text': text,
			'upper': page.upper,
			'children': list(page.children.all()),
		})
		return render(request, 'page.html', params)
