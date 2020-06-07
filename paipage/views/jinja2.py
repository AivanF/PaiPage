__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from jinja2 import Environment
from django.conf import settings

from paipage import config


def make_env(**options):
	env = Environment(**options)
	env.globals.update({
		'config': config,
	})
	return env
