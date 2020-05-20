__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import os, sys

from .const import REQUIRED_STRINGS

config = None


class Language:
	def __init__(self, code, strings):
		self.code = code
		for key in REQUIRED_STRINGS:
			assert key in strings, f'No string "{key}" for lang "{code}"'
		self.strings = strings


class Configurate:
	def __init__(self,
			settings_name,
			site_name,
			template_page_default='pg-usual',
			template_layout_default='lo-menu-top',
			language_default=None,
			language_available=None,
			logger=None,
			):
		global config
		if config is not None:
			raise ValueError(f'PaiPage config collision')
		config = self

		assert isinstance(site_name, str) and len(site_name) > 0
		self.site_name = site_name

		self.template_page_default = template_page_default
		self.template_layout_default = template_layout_default

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
