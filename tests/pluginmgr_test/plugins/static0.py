
from pluginmgr.config import PluginBase
from pluginmgr_test import plugin


@plugin.register('static0')
class Static0(PluginBase):
    pass
