
# pluginmgr


[![PyPI](https://img.shields.io/pypi/v/pluginmgr.svg?maxAge=3600)](https://pypi.python.org/pypi/pluginmgr)
[![Travis CI](https://img.shields.io/travis/20c/pluginmgr.svg?maxAge=3600)](https://travis-ci.org/20c/pluginmgr)
[![Code Health](https://landscape.io/github/20c/pluginmgr/master/landscape.svg?style=flat)](https://landscape.io/github/20c/pluginmgr/master)
[![Codecov](https://img.shields.io/codecov/c/github/20c/pluginmgr/master.svg?maxAge=3600)](https://codecov.io/github/20c/pluginmgr)
[![Requires.io](https://img.shields.io/requires/github/20c/pluginmgr.svg?maxAge=3600)](https://requires.io/github/20c/pluginmgr/requirements)


lightweight python plugin system supporting config inheritance


## To use

There is a full example at <https://github.com/20c/pluginmgr/tree/master/tests/pluginmgr_test>

Create the manager, for example in a module `__init__.py` file

```python
import pluginmgr

# this is the namespace string that import uses
namespace = 'pluginmgr_test.plugins'

# directories to look in, string or list of strings
searchpath = 'path/to/search/in'

# determines if this should create a blank loader to import through. This
# should be enabled if there isn't a real module path for the namespace and
# disabled for sharing the namespace with static modules
# default is False
create_loader = False

plugin = pluginmgr.PluginManager(namespace, searchpath, create_loader)
```

Create and register a plugin, note the filename needs to be the same as registered name

```python
from pluginmgr_test import plugin


# register a plugin named mod0
@plugin.register('mod0')
class Mod0(pluginmgr.PluginBase):
    pass
```

See the dict containing all registered plugins

```python
from pluginmgr_test import plugin

# dict of all registered plugins
print(plugin.registry)
```

