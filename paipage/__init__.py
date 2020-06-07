__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import os, sys
import shutil
import re

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
		template_page_default='pg-pure',
		template_layout_default='lo-pure',
		language_default=None,
		language_available=None,
		plugin_enabled=['simple'],
		logger=None,
		):

	'''
		Basic setup
	'''
	assert isinstance(site_name, str) and len(site_name) > 0
	config.site_name = site_name

	config.template_page_default = template_page_default
	config.template_layout_default = template_layout_default
	config.template_page_list = []
	config.template_layout_list = []

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

	def collect_plugins(search_dir):
		search_dir = os.path.join(search_dir, 'plugins')
		if not os.path.exists(search_dir):
			return
		for plugin_name in os.listdir(search_dir):
			plugin_dir = os.path.join(search_dir, plugin_name)
			if not os.path.isdir(plugin_dir):
				continue

			template_page_list = []
			template_layout_list = []

			# Load list of templates
			location = os.path.join(plugin_dir, 'templates')
			if os.path.exists(location):
				for filename in os.listdir(location):
					match = re.findall(r'^(pg-.+)\.html$', filename)
					if len(match) == 1:
						template_page_list.append(match[0])
					match = re.findall(r'^(lo-.+)\.html$', filename)
					if len(match) == 1:
						template_layout_list.append(match[0])

			config.plugin_installed[plugin_name] = {
				'name': plugin_name,
				'path': plugin_dir,
				'template_page_list': template_page_list,
				'template_layout_list': template_layout_list,
			}
			

	PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(settings.__file__)))
	collect_plugins(PAIPAGE_PATH)
	collect_plugins(PROJECT_PATH)


	'''
		Plugins enabling
	'''
	# TODO: load enabled plugins from stored settings
	config.plugin_enabled = ['primary'] + plugin_enabled
	config.common_css = []

	template_dirs = []
	static_dirs = []

	def add_common_css(plugin_dir, plugin_name, filename):
		src = os.path.join(plugin_dir, 'static', filename)
		res = f'_pai-{plugin_name}-{filename}'
		if os.path.exists(src):
			# TODO: copy to STATIC_ROOT if not DEBUG
			shutil.copyfile(src, os.path.join(plugin_dir, 'static', res))
			config.common_css.append(res)

	for plugin_name in config.plugin_enabled:
		if plugin_name not in config.plugin_installed:
			raise ValueError(f'Missing enabled plugin "{plugin_name}"')
		plugin_info = config.plugin_installed[plugin_name]
		plugin_dir = plugin_info['path']

		location = os.path.join(plugin_dir, 'templates')
		if os.path.exists(location):
			template_dirs.append(location)

		location = os.path.join(plugin_dir, 'static')
		if os.path.exists(location):
			static_dirs.append(location)

		add_common_css(plugin_dir, plugin_name, 'main.css')

		for name in plugin_info['template_page_list']:
			if name not in config.template_page_list:
				config.template_page_list.append(name)

		for name in plugin_info['template_layout_list']:
			if name not in config.template_layout_list:
				config.template_layout_list.append(name)


	'''
		Django settings
	'''
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
