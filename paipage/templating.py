__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.http import HttpResponse

from paipage.const import HTML_EXT
from paipage import config

__all__ = [
	'TemplateHandler',
	'should_show', 'render_page_short', 'render_page_full',
]


class TemplateHandler():
	# PAF elements list with additional page settings
	form_elements = None

	def __init__(self, template, page, text, params):
		# Argument list may be changed, don't override or use *args, **kwargs
		self.template = template
		self.page = page
		self.text = text
		self.params = params
		self.lang = params['lang']
		self.request = params['request']

	def should_show(self):
		return len(self.text.text_full) > 1

	def get_short(self):
		# Must return HTML string
		return self.text.text_short

	def render_full(self):
		# Must return django.http.HttpResponse
		return HttpResponse(self.params.render_file(self.template))

	def __repr__(self):
		return f'{self.__class__.__name__} for "{self.page.url}" {self.lang}'


def _ensure_pg(page):
	template = page.template
	if not template:
		template = config.template_page_default
	return template


def _ensure_lo(page):
	layout = page.layout
	if not layout:
		layout = config.template_layout_default
	return layout


def _get_handler(params, page, text):
	template = _ensure_pg(page)
	if template in config.template_handlers:
		handler_class = config.template_handlers[template]
	else:
		handler_class = TemplateHandler

	return handler_class(
		template, page, text, params
	)


def should_show(params, page, text):
	handler = _get_handler(params, page, text)
	return handler.should_show()


def render_page_short(params, page, text):
	handler = _get_handler(params, page, text)
	return handler.get_short()


def render_page_full(params, page, text):
	handler = _get_handler(params, page, text)
	template = handler.template
	layout = _ensure_lo(page)
	layout += HTML_EXT

	params.update({
		'current': page,
		'handler': handler,
		'text': text,
		'upper': page.upper,
		'children': list(page.children.all()),
		'layout_template': layout,
	})
	return handler.render_full()
