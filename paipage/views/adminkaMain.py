__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from paipage import config
from paipage.models import GlobalSetting

from .params import Params


class AdminkaMainView(View):
	@method_decorator(staff_member_required)
	def get(self, request):
		params = Params(request)
		params['site_name'] = config.site_name
		params['debug'] = settings.DEBUG
		return params.render('am-main')


class AdminkaPluginsView(View):
	@method_decorator(staff_member_required)
	def get(self, request):
		params = Params(request)
		params.scripted['plugin_installed'] = {
			name: config.plugin_installed[name].as_dict()
			for name in config.plugin_installed
		}
		params.scripted['plugin_enabled'] = config.plugin_enabled
		return params.render('am-plugins')
