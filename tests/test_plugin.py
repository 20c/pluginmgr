import pytest

import pluginmgr

config = {
    "plugin": [
        {
            "name": "fancy_probe",
            "type": "probe0",
            "var0": 24,
            "str0": "reeb",
            "interval": "5s",
        },
        {
            "name": "emit0",
            "type": "emit0",
            "var0": 42,
            "str0": "beer",
        },
        {
            "name": "fancy_copy",
            "type": "fancy_probe",
            "var0": 12345,
        },
    ],
}

anon_config = {
    "type": "plugin0",
    "var0": 999,
}


searchpath = ""
plugin = pluginmgr.PluginManager("pluginmgr.tests", searchpath)


class EmitBase(object):
    pass


class ProbeBase(object):
    pass


@plugin.register("plugin0")
class Plugin0(object):
    pass


def test_plugin_registry():
    assert Plugin0 == plugin.get_plugin_class("plugin0")
    with pytest.raises(ValueError):
        plugin.get_plugin_class("nonexistant")

    with pytest.raises(ValueError):

        @plugin.register("plugin0")
        class p0(object):
            pass
