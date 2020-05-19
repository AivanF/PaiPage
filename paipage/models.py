__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.db import models
from django.contrib.auth.models import User
from django.http import Http404

from paipage import config
from paipage.const import LANG_NO

__all__ = [
	'Page',
	'PageText',
]

dater = '%Y-%m-%d'


class Page(models.Model):
	# Meta info
	upper = models.ForeignKey('self', related_name='children', on_delete=models.PROTECT, null=True, blank=True)

	created = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, related_name='created_pages', on_delete=models.PROTECT, null=False)
	updated = models.DateTimeField(auto_now=True)
	updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=False)

	# Main data
	url = models.CharField(max_length=256, null=False, unique=True)
	public = models.BooleanField(default=True)
	# TODO: make choices
	template = models.CharField(default='', max_length=256, null=False, blank=True)
	layout = models.CharField(default='', max_length=256, null=False, blank=True)

	class Meta:
		unique_together = ('upper', 'url',)

	def get_text(self, lang):
		texts = {t.language: t for t in self.texts.all()}
		if lang in texts:
			return texts[lang]
		elif LANG_NO in texts:
			return texts[LANG_NO]
		else:
			return None

	def __str__(self):
		return repr(self)

	def __repr__(self):
		res = f'{self.pk}. Page "{self.url}" {self.created.strftime(dater)}'
		return res


language_choices = [(LANG_NO, 'NoLang')] + [
	(x.code, x.strings['name'])
	for x in config.language_available.values()
]


class PageText(models.Model):
	# Meta info
	page = models.ForeignKey(Page, related_name='texts', on_delete=models.PROTECT, null=False)

	created = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, related_name='created_texts', on_delete=models.PROTECT, null=False)
	updated = models.DateTimeField(auto_now=True)
	updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=False)

	# Main data
	language = models.CharField(max_length=16, choices=language_choices)
	title = models.CharField(max_length=256)
	keywords = models.CharField(max_length=256)
	description = models.TextField()
	text_short = models.TextField()
	text_full = models.TextField()

	class Meta:
		unique_together = ('page', 'language',)

	def __str__(self):
		return repr(self)

	def __repr__(self):
		return f'{self.pk}. Text "{self.page.url}" / "{self.language}" {self.updated.strftime(dater)}'
