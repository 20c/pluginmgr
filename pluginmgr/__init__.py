
import collections
import importlib
import logging
import munge.util
import re
import sys


class SearchPathImporter(object):
    # XXX search path
    def __init__(self, namespace, searchpath):
        self.log = logging.getLogger(__name__)
        self.re_ns = re.compile("%s\.(.*)$" % re.escape(namespace))
        self.searchpath = searchpath

    # import hooks
    def find_module(self, fullname, path=None):
        self.log.debug("hook.find(%s, %s)", fullname, path)
        m = self.re_ns.match(fullname)
        if not m:
            return

        name = m.group(1)
        self.log.debug("hook.found %s", name)
        return

#        print "hook, internal cache", self._class
#        if name in self._class:
#            return self

    def load_module(self, name):
        self.log.debug("hook.load(%s)", name)
        if name in sys.modules:
            return sys.modules[name]

        raise ImportError(name)


class PluginBase(object):
    def __init__(self, config):
        self.config = config
        self.init()

    def init(self):
        pass


class PluginManager(object):
    def __init__(self, namespace, searchpath=None):
        self._class = {}
        self._instance = {}
        self.log = logging.getLogger(__name__)
        self.namespace = namespace

        #sys.meta_path.append(self)
# XXX move to method?
        self.__imphook = SearchPathImporter(namespace, searchpath)
        sys.meta_path.append(self.__imphook)

    def register(self, typ):
        """ register a plugin """
    # should be able to combine class/instance namespace, and inherit from either
    # would need to store meta or rely on copy ctor
        def _func(cls):
            if typ in self._class:
                raise ValueError("duplicated type name '%s'" % typ)
            cls.plugin_type = typ
            self._class[typ] = cls
            return cls
        return _func

    # if plugins can be probes or output, define characteristics, then could use same instance for both

    def get_plugin_class(self, typ):
        if typ in self._class:
            return self._class[typ]

        # try to import by same name
        try:
            importlib.import_module("%s.%s" % (self.namespace, typ))
            if typ in self._class:
                return self._class[typ]

        except ImportError as e:
            self.log.debug("ImportError " + str(e))

        raise ValueError("unknown plugin '%s'" % typ)

# config plugin only
    def _ctor(self, typ, config):
        self.log.debug("ctor: self._instance %s", str(self._instance))
        self.log.debug("ctor: self._class %s", str(self._class))
        if typ in self._instance:
            # get class type, copy config, override with passed config
            obj = self._instance[typ]
            cp = obj.config.copy()
            munge.util.recursive_update(cp, config)
            return type(obj)(cp)
        # try to load
        return self.get_plugin_class(typ)(config)
    # FIXME - raise error, list configured class/instance

# config plugin only
    def new_plugin(self, config):
        """ instantiate a plugin """
    #    if 'type' not in config:
    #        raise ValueError("unknown plugin type '%s'" % str(config))

        obj = None

        # if type is defined, create a new instance
        if 'type' in config:
            typ = config['type']
            obj = self._ctor(typ, config)

    # XXX does not check for mapping, len() could be a str
        # single key is overriding an existing plugin instance
        elif len(config) == 1:
            # get type name and shift out config to parent level
            (typ, config) = config.items()[0]
            obj = self._ctor(typ, config)

        # need to check for None, Greenlets return False
        if obj is None:
            raise ValueError("unable to instantiate plugin from %s" % str(config))

        # store if named
        if 'name' in config:
            obj.name = config['name']
            self._instance[obj.name] = obj
        else:
            # this could dupe on .name, make name=''?
            obj.name = typ

        return obj

# config plugin only
    def get_instance(self, node):
        """ get plugin instance from config node """
        # string is a ref to an existing plugin instance
        if isinstance(node, basestring):
            if node in self._instance:
                return self._instance[node]
            # if not an instance, try for init with empty config
            return self.new_plugin({'type': node})

        if isinstance(node, collections.Mapping):
            return self.new_plugin(node)

        raise ValueError("unable to parse plugin for output %s" % str(node))

    def instantiate(self, config):
        """ takes plugin config (list under 'plugin') and instantiates defined plugins """
        for plugin in config:
            self.new_plugin(plugin)

