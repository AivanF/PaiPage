__title__ = 'PaiPaige Simple plugin'
__version__ = '1.0'
__license__ = 'GPL-3.0'
__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'
description = 'Provides simple yet handy templates.'

from django.http import HttpResponse

from paipage import TemplateHandler


class PgLabeled(TemplateHandler):
	form_elements = [
		{
			'type': 'str',
			'max_len': '32',
			'code': 'label',
			'name': 'Label',
		}, {
			'type': 'str',
			'max_len': '128',
			'code': 'tags',
			'name': 'Tags',
			# TODO: add PAF type "words" to remove bad symbols
		},
	]


class PgNested(TemplateHandler):
	def get_children(self):
		# TODO: filter by lang
		return self.page.children

	def should_show(self):
		return self.get_children.count() > 0


class PgCluster(PgNested):
	form_elements = [
		{
			'type': 'select',
			'subtype': 'page',
			'allow_clear': True,
			'code': 'target',
			'name': 'Target page cluster',
		}, {
			'type': 'str',
			'max_len': '128',
			'code': 'tags',
			'name': 'Tags filter',
			# TODO: add PAF type "words" to remove bad symbols
		}, {
			'type': 'int',
			'min': '0',
			'code': 'count',
			'name': 'Max count',
			'desc': '0 value means no limit',
		}, {
			'type': 'bool',
			'code': 'desc',
			'name': 'Label order',
			'on': 'descending',
			'off': 'ascending',
			'default': True,
		},
	]

	def get_children(self):
		# TODO: filter by lang
		# TODO: filter by tags if set
		# TODO: order by label
		# TODO: limit by count
		return self.page.children


class PgContents(PgNested):

	def get_short(self):
		self.params.update({
			'children': list(self.page.children.all()),
		})
		text = ''
		if len(self.text.text_short) > 1:
			text = self.text.text_short

		template = f'''
{{% import "_utils.html" as utils with context %}}
{{{{ utils.page_contents(children, 2) }}}}
{text}
'''
		return self.params.render_str(template)


template_handlers = {
	'pg-usual': PgLabeled,
	'pg-cluster': PgCluster,
	'pg-contents': PgContents,
}
