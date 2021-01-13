from pluginmgr_test import plugin

import pluginmgr.config


class PluginBase(pluginmgr.config.PluginBase):
    def __init__(self, config, *args, **kwargs):
        super(PluginBase, self).__init__(config)
        self.args = args
        self.kwargs = kwargs


@plugin.register("static0")
class Static0(PluginBase):
    pass
