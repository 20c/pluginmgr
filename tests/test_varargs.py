
import logging
import os
import pytest
import sys


# log here to see import logs
logging.basicConfig(level=logging.DEBUG)


import pluginmgr
import pluginmgr_test

from pluginmgr_test import plugin


config = {'fake': 'config'}
typconf = config.copy()
typconf.update({'type': 'static0'})
args = (1, 2, 5, 'three sir')
kwargs = {'feast': 'lambs', 'and': 'cereals'}


def test_no_varargs():
    Static0 = plugin.get_plugin_class('static0')
    obj = Static0(config)
    assert config == obj.pluginmgr_config
    assert not obj.args
    assert not obj.kwargs


def test_args():
    Static0 = plugin.get_plugin_class('static0')
    obj = Static0(config, 1, 2, 5, 'three sir')
    assert config == obj.pluginmgr_config
    assert args == obj.args
    assert not obj.kwargs


def test_kwargs():
    Static0 = plugin.get_plugin_class('static0')
    obj = Static0(config, **kwargs)
    assert config == obj.pluginmgr_config
    assert not obj.args
    assert kwargs == obj.kwargs


def test_both():
    Static0 = plugin.get_plugin_class('static0')
    obj = Static0(config, *args, **kwargs)
    assert config == obj.pluginmgr_config
    assert args == obj.args
    assert kwargs == obj.kwargs


def test_new_plugin_type():
    obj = plugin.new_plugin(typconf, *args, **kwargs)
    assert typconf == obj.pluginmgr_config
    assert args == obj.args
    assert kwargs == obj.kwargs


def test_new_plugin():
    obj = plugin.new_plugin({'static0': config}, *args, **kwargs)
    assert config == obj.pluginmgr_config
    assert args == obj.args
    assert kwargs == obj.kwargs


def test_get_instance_anonymous():
    obj = plugin.get_instance(typconf, *args, **kwargs)
    assert typconf == obj.pluginmgr_config
    assert args == obj.args
    assert kwargs == obj.kwargs


def test_instantiate():
    nconf = config.copy()
    nconf.update({'name': 'test_instantiate'})
    plugin.instantiate([{'static0': nconf}], *args, **kwargs)
    obj = plugin.get_instance('test_instantiate')
    assert nconf == obj.pluginmgr_config
    assert args == obj.args
    assert kwargs == obj.kwargs

    # test named type inherit / copy
    ntype_conf = nconf.copy()
    ntype_conf.update({'type': 'test_instantiate'})
    obj = plugin.new_plugin(ntype_conf, *args, **kwargs)
    assert ntype_conf == obj.pluginmgr_config
    assert args == obj.args
    assert kwargs == obj.kwargs

