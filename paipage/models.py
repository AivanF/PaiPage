__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import cachetools

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

	def as_dict(self):
		return {
			'pk': self.pk,
			'url': self.url,
			'public': self.public,
			'template_page': self.template,
			'template_layout': self.layout,
			'upper': self.upper.pk if self.upper else None,
		}

	@classmethod
	@cachetools.cached(cache=cachetools.TTLCache(maxsize=8, ttl=10))
	def get_all(cls):
		result = {
			p.pk: {
				**p.as_dict(),
				'langs': [],
				'lang_no': False,
				'titles': {},
			} for p in Page.objects.all()
		}
		for t in PageText.objects.all():
			if t.language == LANG_NO:
				result[t.page.pk]['lang_no'] = True
			else:
				result[t.page.pk]['langs'].append(t.language)
			result[t.page.pk]['titles'][t.language] = t.title
		return result

	def __str__(self):
		return repr(self)

	def __repr__(self):
		result = f'{self.pk}. Page "{self.url}" {self.updated.strftime(dater)}'\
			f' langs: {self.texts.count()}'
		return result


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

	def as_dict(self):
		return {
			'language': self.language,
			'title': self.title,
			'keywords': self.keywords,
			'description': self.description,
			'text_short': self.text_short,
			'text_full': self.text_full,
		}

	def __str__(self):
		return repr(self)

	def __repr__(self):
		return f'{self.pk}. Text "{self.page.url}" / "{self.language}" {self.updated.strftime(dater)}'
