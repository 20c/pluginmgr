import logging

import pluginmgr_test.plugins
import pytest

# log here to see import logs
logging.basicConfig(level=logging.DEBUG)

import pluginmgr_test


def test_import_external_no_keyerror():
    try:
        pluginmgr_test.plugin.import_external()
    except KeyError:
        pytest.fail("KeyError was raised when it should not have been.")
