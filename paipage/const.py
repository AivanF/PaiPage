
from django.conf import settings


def dedupe(items):
	seen = set()
	for item in items:
		if item not in seen:
			yield item
			seen.add(item)


RE_PG_FILE = r'^(pg-.+)\.html$'
RE_LO_FILE = r'^(lo-.+)\.html$'
RE_PG_NAME = r'^(pg-.+)$'
RE_LO_NAME = r'^(lo-.+)$'

HTML_EXT = '.html'
PATH_INDEX = 'index'

LANG_NO = '_'

LANG_KEY = 'lang'

REQUIRED_STRINGS = (
	'name',  # lang name
	'languages',  # lang selection menu
	'error404',  # for bad URLs
	'errorNoLang',  # for pages with no text in current lang
	'back',  # "Back" link
)


class Language:
	def __init__(self, code, strings):
		self.code = code
		for key in REQUIRED_STRINGS:
			assert key in strings, f'No string "{key}" for lang "{code}"'
		self._strings = strings

	def as_dict(self):
		return self._strings

	def __setitem__(self, key, item):
		self._strings[key] = item

	def __getitem__(self, key):
		if key in self._strings:
			return self._strings[key]
		else:
			txt = f'Missing string "{key}"'
			if settings.DEBUG:
				raise KeyError(txt)
			else:
				return f'[ {txt} ]'


lang_en = Language(
	code='en',
	strings=dict(
		name='English',
		languages='Other languages',
		error404='Page not found',
		error500='Server error :(',
		errorNoLang='Not available in this language',
		back='Back',
	),
)
lang_ru = Language(
	code='ru',
	strings=dict(
		name='Русский',
		languages='Другие языки',
		error404='Страница не найдена',
		error500='Ошибка сервера :(',
		errorNoLang='Недоступно на этом языке',
		back='Назад',
	),
)
