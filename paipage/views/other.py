__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import traceback

from django.shortcuts import render_to_response

from paipage import config, const

from .viewUtils import Params

__all__ = [
	'handler404', 'handler500',
]


def handler404(request, *args, **argv):
	params = Params(request)
	layout = config.template_layout_default + const.HTML_EXT
	params.update({
		'layout_template': layout,
		'title': config.language_available[params['lang']].strings['error404'],
		'description': '',
	})
	response = render_to_response('ot-output.html', params.prepare())
	response.status_code = 404
	return response


def handler500(request, *args, **argv):
	params = Params(request)
	layout = config.template_layout_default + const.HTML_EXT
	params.update({
		'layout_template': layout,
		'title': config.language_available[params['lang']].strings['error500'],
		'description': '',
	})
	response = render_to_response('ot-output.html', params.prepare())
	response.status_code = 500
	return response
