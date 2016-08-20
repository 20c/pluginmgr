
import logging
import os
import pytest
import sys


# log here to see import logs
logging.basicConfig(level=logging.DEBUG)


import pluginmgr
import pluginmgr_test


@pytest.yield_fixture(autouse=True)
def set_loader():
    pluginmgr_test.set_create_loader(True)
    yield


def test_static_import():
    # NOTE this will fail if pytest-xdist --boxed isn't used because py.test
    # has already loaded static0 so # it's in the module cache
    with pytest.raises(ImportError):
        from pluginmgr_test.plugins import static0


def test_load_fail():
    with pytest.raises(ImportError):
        pluginmgr_test.plugin._imphook.load_module('does.not.exist')


def test_dyn_import():
    from pluginmgr_test.plugins import mod0

