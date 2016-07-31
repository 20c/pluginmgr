
import logging
import os
import pytest
import sys


# log here to see import logs
logging.basicConfig(level=logging.DEBUG)


import pluginmgr
import pluginmgr_test


@pytest.yield_fixture(autouse=True)
def disable_loader():
    pluginmgr_test.set_create_loader(False)
    yield


def test_static_import():
    from pluginmgr_test.plugins import static0
    assert static0
    from pluginmgr_test.plugins import static0
    assert static0


def test_dyn_import():
    from pluginmgr_test.plugins import mod0

