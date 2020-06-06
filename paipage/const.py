
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
		self.strings = strings


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
		errorNoLang='Не доступно на этом языке',
		back='Назад',
	),
)
