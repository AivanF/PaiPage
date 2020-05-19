__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.conf import settings

from paipage import config


def make_env(**options):
	env = Environment(**options)
	env.globals.update({
		'config': config,
		# TODO: is it needed?
		'static': staticfiles_storage.url,
		'url': reverse,
	})
	return env
