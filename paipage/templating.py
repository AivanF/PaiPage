__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'


from paipage.const import HTML_EXT
from paipage import config


class TemplateHandler():
	def __init__(self, template, page, text, params):
		# Argument list may be changed, don't override or use *args, **kwargs
		self.template = template
		self.page = page
		self.text = text
		self.params = params
		self.lang = params['lang']
		self.request = params['request']

	def get_short(self):
		# Must return HTML string
		return self.text.text_short

	def get_full(self):
		# Must return django.http.HttpResponse
		return self.params.render(self.template)


def render_page_short(params, page, text):
	template = page.template
	if not template:
		template = config.template_page_default

	if template in config.template_handlers:
		handler = config.template_handlers[template](
			template, page, text, params
		)
		return handler.get_short()

	return text.text_short


def render_page_full(params, page, text):
	template = page.template
	if not template:
		template = config.template_page_default

	layout = page.layout
	if not layout:
		layout = config.template_layout_default
	layout += HTML_EXT

	params.update({
		'current': page,
		'text': text,
		'upper': page.upper,
		'children': list(page.children.all()),
		'layout_template': layout,
	})

	if template in config.template_handlers:
		handler = config.template_handlers[template](
			template, page, text, params
		)
		return handler.get_full()

	return params.render(template)
