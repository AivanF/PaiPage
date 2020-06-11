__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import json

from paipage import config
from paipage.const import LANG_KEY, PATH_INDEX, HTML_EXT
from paipage.models import Page


class Params():
	def __init__(self, request):
		lang = None
		if LANG_KEY in request.session:
			lang = request.session[LANG_KEY]
		if lang not in config.language_available:
			lang = config.language_default
			request.session[LANG_KEY] = lang

		root = Page.objects.filter(url=PATH_INDEX).first()
		if root is None:
			txt = f'No root page found! Create a page for url "{PATH_INDEX}"'
			config.logger.error(txt)
			raise ValueError(txt)

		self.params = {
			'request': request,
			'lang': lang,
			'strings': config.language_available[lang].as_dict(),
			'current': None,
			'sections': list(root.children.all()),
			'layout_template': config.template_layout_default + HTML_EXT,
		}
		self.selectables = {}
		self.scripted = {'selectables': self.selectables}

	def __setitem__(self, key, item):
		self.params[key] = item

	def __getitem__(self, key):
		return self.params[key]

	def update(self, adict):
		self.params.update(adict)

	def prepare(self):
		self.params['scripted'] = {}
		for key in list(self.scripted.keys()):
			self.params['scripted'][key] = json.dumps(self.scripted[key], indent=4, sort_keys=True)
		return self.params
