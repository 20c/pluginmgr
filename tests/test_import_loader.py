import importlib
import logging
import os
import sys

import pytest

# log here to see import logs
logging.basicConfig(level=logging.DEBUG)


import pluginmgr_test

import pluginmgr


@pytest.fixture(autouse=True)
def set_loader():
    pluginmgr_test.set_create_loader(True)
    yield


def test_static_import():
    # skip this test for version 3+ since boxed(now forked) doesn't seem to be working and
    # it's only for created loaders
    if sys.version_info[0] >= 3:
        return

    # NOTE this will fail if pytest-xdist --boxed (now forked) isn't used because py.test
    # has already loaded static0 so it's in the module cache
    with pytest.raises(ImportError):
        from pluginmgr_test.plugins import static0


def test_load_fail():
    with pytest.raises(ImportError):
        pluginmgr_test.plugin._imphook.load_module("does.not.exist")


def test_load_file_not_found():
    with pytest.raises(ImportError):
        pluginmgr_test.plugin._imphook.load_module("pluginmgr_test.plugins.nonexistant")


def test_dyn_import():
    from pluginmgr_test.plugins import mod0


def test_standalone_import():
    hook = pluginmgr.SearchPathImporter(
        "standalone",
        os.path.join(os.path.dirname(__file__), "data", "standalone"),
        True,
    )
    sys.meta_path.append(hook)
    mod = importlib.import_module("standalone.mod0.submodule")
    assert mod.test == 1
