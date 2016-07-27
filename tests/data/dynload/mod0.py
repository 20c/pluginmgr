
import pluginmgr
from pluginmgr_test import plugin


@plugin.register('mod0')
class Mod0(pluginmgr.PluginBase):
    pass



