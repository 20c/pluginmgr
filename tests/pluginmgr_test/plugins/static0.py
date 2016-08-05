
import pluginmgr
from pluginmgr_test import plugin


@plugin.register('static0')
class Static0(pluginmgr.PluginBase):
    pass

