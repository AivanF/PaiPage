__title__ = 'PaiPaige Simple plugin'
__version__ = '1.0'
__license__ = 'GPL-3.0'
__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'
description = 'Provides simple yet handy templates.'

from paipage import TemplateHandler


class PgNested(TemplateHandler):
	def should_show(self):
		# TODO: return self.page.children.count() > 0, but check langs
		return True


class PgContents(PgNested):

	def get_short(self):
		self.params.update({
			'children': list(self.page.children.all()),
		})
		text = ''
		if len(self.text.text_short) > 1:
			text = self.text.text_short + '<br>'

		template = f'''
{{% import "_utils.html" as utils with context %}}
{text}
{{{{ utils.page_contents(children, 2) }}}}
<br><br>
'''
		return self.params.render_str(template)

	def get_full(self):
		return self.params.render(self.template)


template_handlers = {
	'pg-cluster': PgNested,
	'pg-contents': PgContents,
}
