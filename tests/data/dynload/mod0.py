
import pluginmgr
import pluginmgr_test


# XXX need common plugin base
plugin = pluginmgr.PluginManager('pluginmgr_test.plugins')

@plugin.register('mod0')
class Mod0(pluginmgr.PluginBase):
    pass



