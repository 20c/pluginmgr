import os
import pluginmgr


path = os.path.join(os.getcwd(), 'tests', 'data', 'dynload')
plugin = pluginmgr.PluginManager('pluginmgr_test.plugins', path, False)


def set_create_loader(value=True):
    plugin._imphook.create_loader = value

