import logging
import os
import sys

import pytest

# log here to see import logs
logging.basicConfig(level=logging.DEBUG)


import pluginmgr_test

import pluginmgr


@pytest.fixture(autouse=True)
def disable_loader():
    pluginmgr_test.set_create_loader(False)
    yield


def test_static_import():
    from pluginmgr_test.plugins import static0

    assert static0
    from pluginmgr_test.plugins import static0

    assert static0


def test_import_nonexistant():
    with pytest.raises(ImportError):
        from pluginmgr_test.plugins import nonexistant


def test_dyn_import():
    from pluginmgr_test.plugins import mod0

    assert mod0
    assert "pluginmgr_test.plugins.mod0" in sys.modules
