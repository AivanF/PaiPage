__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.apps import AppConfig

from .config import configurate_final


class PaiPaiConfig(AppConfig):
    name = 'paipage'

    def ready(self):
    	print('** PaiPaiConfig is ready!!!')
    	configurate_final()
