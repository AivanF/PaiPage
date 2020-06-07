__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import os, sys

from .const import REQUIRED_STRINGS, Language

__all__ = [
	'config', 'configurate',
]


class Config:
	def __init__(self):
		pass


config = Config()

PAIPAGE_PATH = os.path.dirname(os.path.abspath(__file__))


def configurate(
		settings_name,
		site_name,
		template_page_default='pg-usual',
		template_layout_default='lo-menu-top',
		language_default=None,
		language_available=None,
		logger=None,
		):

	'''
		Basic setup
	'''
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


	'''
		Plugins loading
	'''
	config.plugin_installed = {}
	def collect_plugins(location):
		location = os.path.join(location, 'plugins')
		if not os.path.exists(location):
			return
		for name in os.listdir(location):
			if os.path.isdir(os.path.join(location, name)):
				config.plugin_installed[name] = os.path.join(location, name)

	PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(settings.__file__)))
	collect_plugins(PAIPAGE_PATH)
	collect_plugins(PROJECT_PATH)
	print(f'** Found plugins: {config.plugin_installed}')
	# TODO: load plugins from settings
	config.plugin_enabled = ['primary', 'simple']


	'''
		Django settings
	'''

	template_dirs = []
	static_dirs = []

	for name in config.plugin_enabled:
		location = os.path.join(config.plugin_installed[name], 'templates')
		if os.path.exists(location):
			template_dirs.append(location)

		location = os.path.join(config.plugin_installed[name], 'static')
		if os.path.exists(location):
			static_dirs.append(location)

	settings.INSTALLED_APPS.append('paipage')

	settings.TEMPLATES.append({
		'BACKEND': 'django.template.backends.jinja2.Jinja2',
		'DIRS': template_dirs,
		'APP_DIRS': True,
		'OPTIONS': {
			'environment': 'paipage.views.jinja2.make_env',
			# 'autoescape': False,
		},
	})

	settings.STATICFILES_DIRS.extend(static_dirs)

	settings.SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
