__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import os, sys

# TODO: move to `const`
LANG_NO = '_'
LANG_KEY = 'lang'

config = None


class Language:
	def __init__(self, code, name, error404, errorNoLang):
		self.code = code
		self.name = name
		self.error404 = error404
		self.errorNoLang = errorNoLang


class Configurate:
	def __init__(self,
			settings_name,
			site_name,
			template_default='page.html',
			language_default=None,
			language_available=None,
			logger=None,
			):
		global config
		config = self

		assert isinstance(site_name, str) and len(site_name) > 0
		self.site_name = site_name

		self.template_default = template_default

		for x in language_available:
			assert isinstance(x, Language)
		self.language_available = {x.code: x for x in language_available}
		assert isinstance(language_default, str)
		assert language_default in self.language_available
		self.language_default = language_default

		if logger is None:
			import logging
			logger = logging.getLogger('paipage')
			logger.setLevel(logging.DEBUG)
			console_handler = logging.StreamHandler(sys.stdout)
			formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
			console_handler.setFormatter(formatter)
			logger.addHandler(console_handler)
		self.logger = logger


		# django.conf.settings isn't set yet
		settings = sys.modules[settings_name]

		APP_DIR = os.path.dirname(os.path.abspath(__file__))

		settings.INSTALLED_APPS.append('paipage')

		settings.TEMPLATES.append({
			'BACKEND': 'django.template.backends.jinja2.Jinja2',
			'DIRS': [os.path.join(APP_DIR, 'jemplates')],
			'APP_DIRS': True,
			'OPTIONS': {
				'environment': 'paipage.views.jinja2.make_env',
				# 'autoescape': False,
			}, 
		})

		settings.SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

		# TODO: get installed/selected plugins info
		# TODO: collect static/templates from plugins
		# TODO: make available templates list
