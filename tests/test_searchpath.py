
import logging
import os
import pytest
import sys


# log here to see import logs
logging.basicConfig(level=logging.DEBUG)


import pluginmgr
import pluginmgr_test


def test_searchpath_get_none():
    plugin = pluginmgr.PluginManager('static_only')
    assert not plugin.searchpath


def test_searchpath_update_init():
    plugin = pluginmgr.PluginManager('static_only', create_loader=True)
    plugin.searchpath = pluginmgr_test.plugin.searchpath

    from static_only import mod0
    assert mod0


def test_searchpath_change():
    orig = pluginmgr_test.plugin.searchpath

    pluginmgr_test.plugin.searchpath = None
    with pytest.raises(ImportError):
        from pluginmgr_test.plugins import mod0

    pluginmgr_test.plugin.searchpath = orig
    from pluginmgr_test.plugins import mod0
    assert mod0

