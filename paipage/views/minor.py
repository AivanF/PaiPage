__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import re

from django.shortcuts import redirect
from django.views import View

from paipage import config
from paipage.const import LANG_KEY


class ChangeLangView(View):
    def get(self, request, lang):
        if lang not in config.language_available:
            lang = config.language_default
        request.session[LANG_KEY] = lang

        next = request.GET.get('next')
        print(f'Next is {next}')
        if next is None:
            next = '/'
        else:
            next = re.sub(r'/[a-z]{2}/', f'/{lang}/', next)
        return redirect(next)
