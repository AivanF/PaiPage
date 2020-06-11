__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import os, sys
import importlib
import shutil
import re

from .const import RE_PG_FILE, RE_LO_FILE, REQUIRED_STRINGS, Language
from .jinja2 import make_env


class Config:
	def __init__(self):
		pass


config = Config()

PAIPAGE_PATH = os.path.dirname(sys.modules['paipage'].__file__)


def attr2key(src, dst, src_name, dst_name=None):
	if dst_name is None:
		dst_name = src_name
	if hasattr(src, src_name):
		dst[dst_name] = getattr(src, src_name)


def load_plugin_code(plugin_info):
	plugin_name = plugin_info['name']
	plugin_dir = plugin_info['path']
	code_file = os.path.join(plugin_dir, '__init__.py')
	if os.path.exists(code_file):
		module_name = f'pai_plugin_{plugin_name}'
		module = importlib.machinery.SourceFileLoader(module_name, code_file).load_module()
		attr2key(module, plugin_info, 'template_handlers')
		attr2key(module, plugin_info, '__title__', 'title')
		attr2key(module, plugin_info, '__version__', 'version')
		attr2key(module, plugin_info, '__license__', 'license')
		attr2key(module, plugin_info, '__author__', 'author')
		attr2key(module, plugin_info, '__contact__', 'contact')


def collect_plugins(search_dir):
	search_dir = os.path.join(search_dir, 'plugins')
	if not os.path.exists(search_dir):
		return
	for plugin_name in os.listdir(search_dir):
		plugin_dir = os.path.join(search_dir, plugin_name)
		if not os.path.isdir(plugin_dir):
			continue

		plugin_info = {
			'title': '_unknown_',
			'version': '_unknown_',
			'license': '_unknown_',
			'author': '_unknown_',
			'contact': '_unknown_',
			'name': plugin_name,
			'path': plugin_dir,
			'template_page_list': [],
			'template_layout_list': [],
			'template_handlers': {}
		}

		# Load list of templates
		location = os.path.join(plugin_dir, 'templates')
		if os.path.exists(location):
			for filename in os.listdir(location):
				match = re.findall(RE_PG_FILE, filename)
				if len(match) == 1:
					plugin_info['template_page_list'].append(match[0])
				match = re.findall(r'^(lo-.+)\.html$', filename)
				if len(match) == 1:
					plugin_info['template_layout_list'].append(match[0])

		load_plugin_code(plugin_info)

		config.plugin_installed[plugin_name] = plugin_info


def enable_plugins():
	config.common_css = []
	config.template_dirs = []
	config.static_dirs = []
	config.template_handlers = {}

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
			config.template_dirs.append(location)

		location = os.path.join(plugin_dir, 'static')
		if os.path.exists(location):
			config.static_dirs.append(location)

		add_common_css(plugin_dir, plugin_name, 'main.css')

		for name in plugin_info['template_page_list']:
			if name not in config.template_page_list:
				config.template_page_list.append(name)

		for name in plugin_info['template_layout_list']:
			if name not in config.template_layout_list:
				config.template_layout_list.append(name)

		config.template_handlers.update(plugin_info['template_handlers'])


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
	PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(settings.__file__)))
	collect_plugins(PAIPAGE_PATH)
	# TODO: set as arg `plugin_paths`
	collect_plugins(PROJECT_PATH)


	'''
		Plugins enabling
	'''
	# TODO: load enabled plugins from stored settings
	config.plugin_enabled = ['primary'] + plugin_enabled
	enable_plugins()

	config.jinja2 = make_env(template_dirs=config.template_dirs, config=config)


	'''
		Django settings
	'''
	settings.INSTALLED_APPS.append('paipage')
	settings.STATICFILES_DIRS.extend(config.static_dirs)
	settings.SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'