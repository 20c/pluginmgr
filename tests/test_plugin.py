
import pytest

import pluginmgr

config = {
    'plugin': [
        {
        'name': 'fancy_probe',
        'type': 'probe0',
        'var0': 24,
        'str0': 'reeb',
        'interval': '5s',
        },
        {
        'name': 'emit0',
        'type': 'emit0',
        'var0': 42,
        'str0': 'beer',
        },
        {
        'name': 'fancy_copy',
        'type': 'fancy_probe',
        'var0': 12345,
        },
    ],
}

anon_config = {
    'type': 'plugin0',
    'var0': 999,
}


searchpath = ''
plugin = pluginmgr.PluginManager('pluginmgr.tests', searchpath)

class PluginBase(pluginmgr.PluginBase):
    pass

class EmitBase(PluginBase):
    pass

class ProbeBase(PluginBase):
    pass

@plugin.register('plugin0')
class Plugin0(PluginBase):
    pass

@plugin.register('emit0')
class EmitPlugin0(EmitBase):
    def emit(self, msg):
        pass

@plugin.register('emit_abc')
class EmitPluginABC(EmitBase):
    # emit not defined to test TypeError
    pass

@plugin.register('probe0')
class TimedPlugin0(ProbeBase):
    pass

@plugin.register('probe1')
class ProbePlugin1(ProbeBase):
    def probe(self):
        return []

def test_plugin_registry():
    assert Plugin0 == plugin.get_plugin_class('plugin0')
    with pytest.raises(ValueError):
        plugin.get_plugin_class('nonexistant')

    with pytest.raises(ValueError):
        @plugin.register('plugin0')
        class p0(PluginBase):
            pass

def test_plugin_instance():
    with pytest.raises(ValueError):
        plugin.new_plugin({})

    with pytest.raises(ValueError):
        plugin.get_instance('nonexistant')
    with pytest.raises(ValueError):
        plugin.get_instance(['unparsable'])

    plugin.instantiate(config['plugin'])
    for each in config['plugin']:
        if 'name' not in each:
            continue
        obj = plugin.get_instance(each['name'])
        for k,v in each.items():
            assert v == obj.config[k]

    obj = plugin.get_instance(anon_config)
    assert obj.config == anon_config

    # copy ctor
    obj = plugin.get_instance('fancy_copy')
    assert 'reeb' == obj.config['str0']

    obj = plugin.get_instance({'fancy_copy': {'var0': 'luggage'}})
    assert 'reeb' == obj.config['str0']

