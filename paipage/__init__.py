__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import os, sys

from .const import REQUIRED_STRINGS, Language


class Config:
	def __init__(self):
		pass


config = Config()


def configurate(
		settings_name,
		site_name,
		template_page_default='pg-usual',
		template_layout_default='lo-menu-top',
		language_default=None,
		language_available=None,
		logger=None,
		):

	assert isinstance(site_name, str) and len(site_name) > 0
	config.site_name = site_name

	config.template_page_default = template_page_default
	config.template_layout_default = template_layout_default

	for x in language_available:
		assert isinstance(x, Language)
	config.language_available = {x.code: x for x in language_available}
	assert isinstance(language_default, str)
	assert language_default in config.language_available
	config.language_default = language_default

	if logger is None:
		import logging
		logger = logging.getLogger('paipage')
		logger.setLevel(logging.DEBUG)
		console_handler = logging.StreamHandler(sys.stdout)
		formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
		console_handler.setFormatter(formatter)
		logger.addHandler(console_handler)
	config.logger = logger


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
