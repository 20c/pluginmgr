
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
args = (1, 2, 5, 'three sir')
kwargs = {'feast': 'lambs', 'and': 'cereals'}


def test_no_varargs():
    Static0 = plugin.get_plugin_class('static0')
    obj = Static0(config)
    assert config == obj.config
    assert not obj.args
    assert not obj.kwargs


def test_args():
    Static0 = plugin.get_plugin_class('static0')
    obj = Static0(config, 1, 2, 5, 'three sir')
    assert config == obj.config
    assert args == obj.args
    assert not obj.kwargs


def test_kwargs():
    Static0 = plugin.get_plugin_class('static0')
    obj = Static0(config, **kwargs)
    assert config == obj.config
    assert not obj.args
    assert kwargs == obj.kwargs


def test_both():
    Static0 = plugin.get_plugin_class('static0')
    obj = Static0(config, *args, **kwargs)
    assert config == obj.config
    assert args == obj.args
    assert kwargs == obj.kwargs


def test_new_plugin_type():
    conf = config.copy()
    conf.update({'type': 'static0'})
    obj = plugin.new_plugin(conf, *args, **kwargs)
    assert conf == obj.config
    assert args == obj.args
    assert kwargs == obj.kwargs


def test_new_plugin():
    obj = plugin.new_plugin({'static0': config}, *args, **kwargs)
    assert config == obj.config
    assert args == obj.args
    assert kwargs == obj.kwargs


