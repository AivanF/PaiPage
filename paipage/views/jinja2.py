__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from jinja2 import Environment
from django.conf import settings

from paipage import config


def safe_json(input):
	return input.replace('</script>', '<\\/script>')


def make_env(**options):
	env = Environment(**options)
	env.filters['safe_json'] = safe_json
	env.globals.update({
		'config': config,
	})
	return env
