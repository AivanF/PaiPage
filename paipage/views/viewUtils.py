__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from paipage import config
from paipage.const import LANG_KEY, PATH_INDEX, HTML_EXT
from paipage.models import Page


def prepare_params(request):
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

	params = {
		'lang': lang,
		'strings': config.language_available[lang].strings,
		'current': None,
		'sections': list(root.children.all()),
		'layout_template': config.template_layout_default + HTML_EXT,
	}
	return params
