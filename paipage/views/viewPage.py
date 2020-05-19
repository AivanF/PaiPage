__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.shortcuts import render
from django.views import View
from django.http import Http404

from paipage import config
from paipage.const import PATH_INDEX, LANG_KEY
from paipage.models import Page


class PageView(View):
	def get(self, request, path=PATH_INDEX):
		lang = None
		if LANG_KEY in request.session:
			lang = request.session[LANG_KEY]
		if lang not in config.language_available:
			lang = config.language_default
			request.session[LANG_KEY] = lang

		page = Page.objects.filter(url=path).first()
		if page is None:
			raise Http404

		text = page.get_text(lang)
		if text is None:
			config.logger.error(f'No lang "{lang}" for page "{path}"')
			# TODO: show "not available" page
			raise Http404

		params = {
			'text': text,
			'lang': lang,
			'upper': page.upper,
			'children': list(page.children.all()),
			'strings': config.language_available[lang].strings,
		}
		return render(request, 'page.html', params)
