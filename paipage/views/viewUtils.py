__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from paipage import config
from paipage.const import LANG_KEY


def prepare_params(request):
	lang = None
	if LANG_KEY in request.session:
		lang = request.session[LANG_KEY]
	if lang not in config.language_available:
		lang = config.language_default
		request.session[LANG_KEY] = lang

	params = {
		'strings': config.language_available[lang].strings,
		'lang': lang,
	}
	return params
